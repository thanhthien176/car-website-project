import logging
import io
import os

from PIL import Image, ImageOps, UnidentifiedImageError
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

def convert_to_webp(image_field, quality=85, max_size=None):
    """Convert image to WebP, resize if necessary, maintain aspect ratio.

    Args:
        image_field (_type_): ImageField instance
        quality (int, optional): WebP quality(1-100), 85 is good balance
        max_size: tuple(with, height) - resize if image is larger
    
    return: ContentFile webp or None if error
    """
    if not image_field:
        return None
    
    try:
        img: Image.Image = Image.open(image_field)
    except (UnidentifiedImageError, OSError) as exc:
        logger.warning("convert_to_webp: could not open image '%s': %s", image_field.name, exc)
        return None
    
    
    # --- Correct EXIF orientation ------------------------------------------------
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass  # Non-fatal; proceed with original orientation.
    
    # Covert into RGBA if needed (png has transparency)
    # RGBA is well supported with WebP
    if img.mode not in ('RGB', 'RGBA'):
        target_mode = "RGBA" if "transparency" in img.info else "RGB"
        img = img.convert(target_mode)
        
    # resize if image is too large - maintain is aspect ratio
    if max_size:
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
    # save into WebP
    output = io.BytesIO()
    save_kwargs = {
        "format": "WEBP",
        "quality": quality,
        "optimize": True,
        "method": 6,
    }
    
    # Keep transparency if it is RGBA
    if img.mode == 'RGBA':
        # lossless=False keeps the alpha channel while still applying lossy
        # compression to the RGB data — best balance for photos-with-alpha.
        save_kwargs["lossless"] = False
    
    try:
        img.save(output, **save_kwargs)
    except Exception as exc:
        logger.warning("convert_to_webp: could not encode '%s' to WebP: %s", image_field.name, exc)
        return None
    
    output.seek(0)
    
    name, ext = os.path.splitext(image_field.name)
    new_name = f"{name}.webp"
    return ContentFile(output.read(), name=new_name)
    
    
    