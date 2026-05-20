from typing import Any

from cars.models import Brand
from .base_import import BaseImportCommand

class Command(BaseImportCommand):
    help = (
        "Import brands from CSV file.\n"
        "Use: python manage.py import_brands <path/to/file.csv>.\n\n"
        "Required columns: name, country_of_origin.\n"
        "Optional columns: founded_year, website, description, is_active"
    )
    
    required_headers = {"name", "country_of_origin"}
    default_stats = {"created": 0, "updated": 0, "skipped": 0, "errors": 0}
    
    def _import_row(self, row: dict[str, str], row_num: int, options: dict[str, Any], stats: dict[str, int]):
        name = self._require_str(row, "name", row_num, stats)
        if name is None:
            return
        
        country = self._require_str(row, "country_of_origin", row_num, stats)
        if country is None:
            return
        
        defaults = {
            "country_of_origin": country,
            "founded_year":     self._to_int(row.get("founded_year"), row_num),
            "website":          self._clean_str(row.get("website")) or None,
            "description":      self._clean_str(row.get("description")),
            "is_active":        self._to_bool(row.get("is_active"))
        }
        
        if options["update"]:
            _, was_created = Brand.objects.update_or_create(name=name, defaults=defaults)
            stats["created" if was_created else "updated"] += 1
        
        else:
            _, was_created = Brand.objects.get_or_create(name=name, defaults=defaults)
            stats["created" if was_created else "skipped"] += 1
    
   