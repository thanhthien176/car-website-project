import os
from django.core.exceptions import ValidationError

def validate_image_size(image):
    limit_mb = 5
    if image.size > limit_mb*1024*1024:
        raise ValidationError(f"The image file size is not exceed {limit_mb}MB")
    
    

def validate_image_extension(image):
    allowed_extension = [".jpg", ".jpeg", ".png", ".webp"]
    ext = os.path.splitext(image.name)[1].lower()
    if ext not in allowed_extension:
        
        raise ValidationError(
            f"Invalid formating: '{ext}'."
            f"Only accept: '{", ".join(allowed_extension)}'"
            )