# management/commands/import_images.py
from django.utils.text import slugify

from cars.models import CarModel, CarVariant, CarImage, VariantImage
from .base_import import BaseImportCommand


class Command(BaseImportCommand):
    help = (
        "Import gallery images for CarModel and/or CarVariant from CSV.\n\n"
        "If the 'variant_name' column has a value -> image is imported into VariantImage\n"
        "  (linked to the corresponding CarVariant).\n"
        "If 'variant_name' is empty (or the variant is not found) -> image is\n"
        "  imported into CarImage (linked to CarModel).\n\n"
        "Usage: python manage.py import_images images.csv\n\n"
        "Required columns: brand_name, model_name, image_url\n"
        "Optional columns: variant_name, caption, is_primary, order,\n"
        "  author_name, author_url, source_name, source_url, license"
    )

    required_headers = {"brand_name", "model_name", "image_url"}
    default_stats = {
        "car_image_created": 0,
        "variant_image_created": 0,
        "skipped": 0,
        "errors": 0,
    }

    _ATTRIBUTION_FIELDS = (
        "author_name", "author_url", "source_name", "source_url", "license",
    )

    def _import_row(self, row, row_num, options, stats):
        brand_name = self._require_str(row, "brand_name", row_num, stats)
        if brand_name is None:
            return

        model_name = self._require_str(row, "model_name", row_num, stats)
        if model_name is None:
            return
        
        model_year = self._require_str(row, "model_year", row_num, stats)
        if model_year is None:
            model_year = '2026'

        image_url = self._require_str(row, "image_url", row_num, stats)
        if image_url is None:
            return

        # ── 1. Find CarModel (must exist) ─────────────────
        model_slug = slugify(f"{brand_name}-{model_name} {model_year}")
        try:
            car_model = CarModel.objects.get(slug=model_slug)
        except CarModel.DoesNotExist:
            self.stdout.write(self.style.WARNING(
                f"  [Row {row_num}] CarModel '{model_slug}' doesn't exist - "
                f"skip. Run import_cars first."
            ))
            stats["skipped"] += 1
            return

        # ── 2. There is variant_name -> try to find CarVariant ────────────────
        variant_name = self._clean_str(row.get("variant_name"))
        variant = None
        if variant_name:
            variant_slug = self._create_slugify(
                f"{brand_name}-{model_name}-{variant_name}"
            )
            try:
                variant = CarVariant.objects.get(slug=variant_slug)
            except CarVariant.DoesNotExist:
                self.stdout.write(self.style.WARNING(
                    f"  [Row {row_num}] CarVariant '{variant_slug}' doesn't exist "
                    f"- fallback to CarImage of CarModel."
                ))
                variant = None

        # ── 3. Field shared for both CarImage / VariantImage ──────
        common_fields = {
            "caption": self._clean_str(row.get("caption")),
            "is_primary": self._to_bool(row.get("is_primary"), default=False),
            "order": self._to_int(row.get("order"), row_num) or 0,
        }
        for field in self._ATTRIBUTION_FIELDS:
            common_fields[field] = self._clean_str(row.get(field))

        # ── 4. Create instance, download image, then save ─────────────────
        if variant is not None:
            image_instance = VariantImage(variant=variant, **common_fields)
            target_label = f"VariantImage for {variant}"
            stat_key = "variant_image_created"
        else:
            image_instance = CarImage(car=car_model, **common_fields)
            target_label = f"CarImage for {car_model}"
            stat_key = "car_image_created"

        success = self._download_image(
            image_instance, "image", image_url, max_size=(1920, 1920)
        )
        if not success:
            self.stdout.write(self.style.WARNING(
                f"  [Row {row_num}] Failed to download image from {image_url} - skip"
            ))
            stats["skipped"] += 1
            return

        image_instance.save()
        stats[stat_key] += 1
        self.stdout.write(f"  + {target_label}")