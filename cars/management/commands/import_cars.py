from django.utils.text import slugify
 
from cars.models import Brand, BodyType, CarClass, CarModel, CarVariant
from .base_import import BaseImportCommand


class Command(BaseImportCommand):
    help=(
        "Import CarModel + CarVariant from CSV file.\n"
        "Used: python manage.py import_cars <path/to/file.csv>\n\n"
        "Required columns: brand_name, model_name\n"
        "Option columns: body_type, car_class, model_year, description,\n"
        "   variant_name, fuel_type, price_min, price_max, is_active"
    )
    required_headers = {"brand_name", "model_name"}
    default_stats = {
        "model_created": 0,
        "model_updated": 0,
        "variant_created": 0,
        "variant_updated": 0,
        "body_type_created": 0,
        "class_created":0,
        "skipped": 0,
        "errors": 0,
    }

                    
    def _import_row(self, row, row_num, options, stats):
        # ── 1. Brand (Must already exist) ───────────────────────────────
        brand_name = self._require_str(row, "brand_name", row_num, stats)
        if not brand_name:
            return
        
        try:
            brand = Brand.objects.get(name=brand_name)
        except Brand.DoesNotExist:
            self.stdout.write(self.style.WARNING(
                f" Row {row_num}: Brand {brand_name} not exists - ignore"
                f"Run import_brands first"
            ))
            stats["skipped"]+= 1
            return
        
        # ── 2. BodyType (get_or_create) ────────────────────────────────
        body_type = None
        body_type_name = self._clean_str(row.get("body_type"))
        if body_type_name:
            body_type, body_type_created = BodyType.objects.get_or_create(
                name = body_type_name,
                defaults={"slug": slugify(body_type_name)}
            )
            if body_type_created:
                stats["body_type_created"] += 1
                
        
        # ── 3. CarClass (get_or_create) ────────────────────────────────
        car_class = None
        car_class_name = self._clean_str(row.get("car_class"))
        if car_class_name:
            car_class, class_created = CarClass.objects.get_or_create(
                name = car_class_name,
                defaults={"slug": slugify(car_class_name)}
            )
            if class_created:
                stats["class_created"] += 1
                self.stdout.write(f" + CarClass: {car_class}")
        
        # ── 4. CarModel ────────────────────────────────────────────────
        model_name = self._clean_str(row.get("model_name"))
        if not model_name:
            self.stdout.write(self.style.WARNING(
                f" Row {row_num}: Missing model_name - ignore"
            ))
            stats["skipped"] += 1
            return
        
        model_defaults = {
            "body_type": body_type,
            "car_class": car_class,
            "model_year": self._to_int(row.get("model_year"), row_num),
            "description": self._clean_str(row.get("description")) or None,
        }
        
        car_model, model_created = CarModel.objects.get_or_create(
            brand=brand,
            name=model_name,
            defaults=model_defaults,
        )
        
        if model_created:
            stats["model_created"] += 1
            self.stdout.write(f" + CarModel: {car_model}")
        elif options["update"]:
            for field, value in model_defaults.items():
                setattr(car_model, field, value)
            
            car_model.save()
            stats["model_updated"] += 1
            self.stdout.write(f" ~ CarModel updated: {car_model}")

        # ── 5. CarVariant (tuỳ chọn) ───────────────────────────────────
        variant_name = row.get("variant_name", "").strip()
        if not variant_name:
            return
        
        fuel_type = self._clean_fuel_type(row.get("fuel_type"), row_num)
            
        variant_defaults = {
            "fuel_type": fuel_type,
            "price_min": self._to_decimal(row.get("price_min", "0"), row_num),
            "price_max": self._to_decimal(row.get("price_max", "0"), row_num),
            "is_active": self._to_bool(row.get("is_active"), default=False),
        }
        
        variant, variant_created = CarVariant.objects.get_or_create(
            car_model = car_model,
            variant_name = variant_name,
            defaults=variant_defaults,
        )
        
        if variant_created:
            stats["variant_created"] += 1
            self.stdout.write(f" + Variant: {variant}")
        elif options["update"]:
            self._apply_update(variant, variant_defaults)
            stats["variant_updated"] += 1
            self.stdout.write(f" ~ Variant updated: {variant}")
    
    # ======= Helper =======
    
    
    def _apply_update(self, instance, fields:dict):
        for field, value in fields.items():
            setattr(instance, field, value)
        instance.save()
        
    def _clean_fuel_type(self, value, row_num) -> str:
        fuel = self._clean_str(value).lower() or "gasoline"
        valid = {k for k, _ in CarVariant.FUEL_TYPE_CHOICES}
        if fuel not in valid:
            self.stdout.write(self.style.WARNING(
                f" Row {row_num}: fuel type is invalid - use 'gasoline'"
            ))
            return "gasoline"
        return fuel
        
        
            