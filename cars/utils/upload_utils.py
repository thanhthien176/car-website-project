import uuid
from pathlib import Path
from django.utils.deconstruct import deconstructible

@deconstructible
class UploadToPath:
    def __init__(self, base_path, sub_path=None):
        self.base_path = base_path
        self.sub_path = sub_path
        
    def __call__(self, instance, filename):
        ext = Path(filename).suffix
        
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        
        sub = f"{self.sub_path}/" if self.sub_path else ""

        return (
            f"{self.base_path}/{sub}{unique_filename}"
        )