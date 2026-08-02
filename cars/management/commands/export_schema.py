# cars/management/commands/export_schema_manifest.py
import json
from django.core.management.base import BaseCommand
from django.apps import apps

SPEC_MODELS = [
    "CarModel", "CarVariant", "DimensionSpecification", "EngineSpecification",
    "PerformanceSpecification", "FuelConsumptionSpecification",
    "ExteriorSpecification", "InteriorSpecification", "SeatSpecification",
    "ComfortSpecification", "SecureSpecification", "SafetySpecification",
]

class Command(BaseCommand):
    def handle(self, *args, **options):
        manifest = {}
        for model_name in SPEC_MODELS:
            model = apps.get_model("cars", model_name)
            fields = []
            exclusion = ["id", "variant", "seo_title", "seo_description", "seo_keyword"]
            for f in model._meta.get_fields():
                if f.concrete and f.name not in exclusion:
                    fields.append({
                        "field_name": f.name,
                        "internal_type": f.get_internal_type(),
                        "help_text": getattr(f, "help_text", "") or "",
                        "choices": getattr(f, "choices", None),
                    })
            manifest[model_name] = fields

        with open("data/schema_manifest.json", "w", encoding="utf-8") as fp:
            json.dump(manifest, fp, ensure_ascii=False, indent=2)