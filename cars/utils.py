from typing import Any

from django.utils.deconstruct import deconstructible

@deconstructible
class UploadToPath:
    def __init__(self, sub_path):
        self.sub_path = sub_path
        
    def __call__(self, instance, filename) -> Any:
        return f"{instance.brand}/{instance.name}/{self.sub_path}/{filename}"