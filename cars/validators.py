import os
from django.core.exceptions import ValidationError

def validate_image_size(image):
    limit_mb = 5
    if image.size > limit_mb*1024*1024:
        raise ValidationError(f"The image file size is not exceed {limit_mb}MB")
    
    
ALLOWED_EXTENSION = {".jpg", ".jpeg", ".png", ".webp"}

def validate_image_extension(image):
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in ALLOWED_EXTENSION:
        
        raise ValidationError(
            f"Invalid formating: '{ext}'."
            f"Only accept: '{", ".join(ALLOWED_EXTENSION)}'"
            )