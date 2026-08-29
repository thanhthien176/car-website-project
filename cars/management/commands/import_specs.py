# management/commands/import_specs.py
"""
Generic importer for ALL one-to-one "specification" models attached to
CarVariant (DimensionSpecification, EngineSpecification, SafetySpecification,
ComfortSpecification, ...).

Design goal: adding a brand-new spec model or a brand-new field on an
existing spec model should require ZERO changes to this file.

How it works
------------
1. Discover spec models automatically:
   Any model in the `cars` app that has a OneToOneField pointing to
   CarVariant is treated as a "spec model". This is exactly how your
   existing models (DimensionSpecification, EngineSpecification, ...)
   are already built, so nothing needs to be registered by hand.

2. Discover importable fields automatically:
   For each spec model, every concrete field (except the pk and the
   OneToOneField itself) is inspected. Its Django field class decides
   which converter from BaseImportCommand to use
   (BooleanField -> _to_bool, IntegerField family -> _to_int,
   DecimalField -> _to_decimal, Char/TextField -> _clean_str).

3. Match against the CSV:
   For every discovered field, if a column with that exact name exists
   in the CSV row AND is non-empty, it gets imported. Otherwise it is
   simply skipped and the model's own default is used. This means a
   single CSV can mix-and-match columns from as many spec models as you
   want, and CSVs that don't cover a given spec model at all are fine.

CSV format
----------
Required column:
    variant_slug        -> slug of an existing CarVariant

Everything else is optional and matched by field name, e.g.:
    variant_slug,length,width,seating_capacity,abs,vsc,airbag,transmission,urban
    toyota-innova-cross-20g,4885,1840,7,true,true,7,cvt,7.5

Usage
-----
    python manage.py import_specs specs.csv
    python manage.py import_specs specs.csv --update      # update existing rows
    python manage.py import_specs specs.csv --dry-run
"""
from django.apps import apps
from django.db import models as djm, transaction
from django.utils.text import slugify

from cars.models import CarVariant
from cars.models.car_models import Brand, CarModel
from .base_import import BaseImportCommand


# Order matters only in the sense that each Django field class below is
# disjoint (a field can't be both BooleanField and DecimalField), so a
# simple isinstance() scan is safe.
_FIELD_CONVERTERS = {
    djm.BooleanField: "_to_bool",
    djm.DecimalField: "_to_decimal",
    djm.IntegerField: "_to_int",          # covers Positive(Small)IntegerField too
    djm.CharField: "_clean_str",
    djm.TextField: "_clean_str",
}


class Command(BaseImportCommand):
    help = (
        "Import data into ANY one-to-one specification model linked to "
        "CarVariant (Dimension/Engine/Performance/FuelConsumption/Exterior/"
        "Interior/Seat/Comfort/Safety, and any future spec model you add).\n\n"
        "Spec models and their fields are discovered automatically via "
        "introspection - you never need to edit this command when you add "
        "a new spec model or a new field to an existing one.\n\n"
        "Required column: variant_slug\n"
        "Optional columns: any field name belonging to any spec model, "
        "e.g. length, width, seating_capacity, abs, vsc, airbag, "
        "transmission, urban, display, sunroof, ..."
    )

    required_headers = {"variant_name", "brand_name", "model_name"}

    # ------------------------------------------------------------------
    # Discovery
    # ------------------------------------------------------------------

    def _discover_spec_models(self):
        """Return [(model, one_to_one_field_name), ...] for every model in
        the 'cars' app that has a OneToOneField pointing at CarVariant."""
        spec_models = []
        for model in apps.get_app_config("cars").get_models():
            for field in model._meta.get_fields():
                if (
                    isinstance(field, djm.OneToOneField)
                    and field.remote_field.model is CarVariant
                ):
                    spec_models.append((model, field.name))
                    break
        return spec_models

    def _importable_fields(self, model, variant_field_name):
        """Return [(field_name, converter_method_name), ...] for fields on
        *model* that we know how to safely convert from a CSV string."""
        fields = []
        for field in model._meta.get_fields():
            if not isinstance(field, djm.Field):
                continue
            if field.name in (variant_field_name, "id"):
                continue
            if field.auto_created:
                continue

            for field_class, converter_name in _FIELD_CONVERTERS.items():
                if isinstance(field, field_class):
                    fields.append((field.name, converter_name))
                    break
        return fields

    # ------------------------------------------------------------------
    # Command lifecycle
    # ------------------------------------------------------------------

    def handle(self, *args, **options):
        self._spec_models = self._discover_spec_models()

        # Build stats dict dynamically: 2 counters per discovered model.
        stats = {"skipped": 0, "errors": 0}
        for model, _ in self._spec_models:
            key = model.__name__.lower()
            stats[f"{key}_created"] = 0
            stats[f"{key}_updated"] = 0
        self.default_stats = stats

        if not self._spec_models:
            self.stdout.write(self.style.WARNING(
                "No spec models found (no model with a OneToOneField to "
                "CarVariant). Nothing to do."
            ))

        super().handle(*args, **options)

    # ------------------------------------------------------------------
    # Row processing
    # ------------------------------------------------------------------

    def _import_row(self, row, row_num, options, stats):
        brand_name = self._require_str(row, "brand_name", row_num, stats)
        model_name = self._require_str(row, "model_name", row_num, stats)
        variant_name = self._require_str(row, "variant_name", row_num, stats)

        try:
            brand = Brand.objects.get(name=brand_name)
        except Brand.DoesNotExist:
            self.stdout.write(self.style.WARNING(
                    f"  [Row {row_num}] Brand '{brand_name}' not found - skipped"
                ))
            stats["skipped"] += 1
            return
            
            
        try:
            car_model = CarModel.objects.get(
                brand=brand,
                name=model_name,
            )
        except CarModel.DoesNotExist:
            self.stdout.write(self.style.WARNING(
                    f"  [Row {row_num}] CarModel '{brand_name} {model_name}' not found - skipped"
                ))
            stats["skipped"] += 1
            return

        try:
            variant = CarVariant.objects.get(
                car_model=car_model,
                name=variant_name,
            )
        except CarVariant.DoesNotExist:
            self.stdout.write(self.style.WARNING(
                f"  [Row {row_num}] CarVariant '{brand_name} {model_name} {variant_name}' not found - skipped"
            ))
            stats["skipped"] += 1
            return

        for model, variant_field_name in self._spec_models:
            self._import_spec_for_model(
                model, variant_field_name, variant, row, row_num, options, stats
            )

    def _import_spec_for_model(
        self, model, variant_field_name, variant, row, row_num, options, stats
    ):
        field_defs = self._importable_fields(model, variant_field_name)

        values = {}
        for field_name, converter_name in field_defs:
            if field_name not in row:
                continue
            raw = row.get(field_name)
            # Check raw if it doesn't has data 
            # then return None with int and decimal to django doesn't use default ""
            is_empty = raw is None or str(raw).strip() == ""
            
            if converter_name in ("_to_int", "_to_decimal"):
                values[field_name] = None if is_empty else getattr(self, converter_name)(raw, row_num)
                continue

            converter = getattr(self, converter_name)
            if converter_name == "_to_bool":
                values[field_name] = converter(raw, default=False)
            else:
                values[field_name] = converter(raw)

        # This CSV row doesn't contain any column relevant to this spec
        # model at all -> don't touch it (don't even create an empty row).
        if not values:
            return

        key = model.__name__.lower()
        try:
            with transaction.atomic():
                obj, created = model.objects.get_or_create(
                    **{variant_field_name: variant},
                    defaults=values,
                )

                if created:
                    stats[f"{key}_created"] += 1
                    self.stdout.write(f"  + {model.__name__} created for {variant}")
                elif options["update"]:
                    for field_name, value in values.items():
                        setattr(obj, field_name, value)
                    obj.save()
                    stats[f"{key}_updated"] += 1
                    self.stdout.write(f"  ~ {model.__name__} updated for {variant}")
                
                else:
                    self.stdout.write(self.style.WARNING(
                        f"  [Row {row_num}] {model.__name__} for {variant} existed, "
                        f"Use --update to overide - ignore"
                    ))
                    
        except Exception as exc:
            self.stdout.write(self.style.ERROR(
            f"  [Row {row_num}] {model.__name__} failed: {exc}"
            ))
            stats["errors"] += 1