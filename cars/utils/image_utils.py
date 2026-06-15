import logging
import io
import os
import requests
import uuid

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
        
        return _image_to_webp(
            img,
            quality,
            max_size,
        )
    except (UnidentifiedImageError, OSError) as exc:
        logger.warning("convert_to_webp: could not open image '%s': %s", image_field.name, exc)
        return None
    

def _image_to_webp(
    img: Image.Image,
    quality: int = 85,
    max_size=None,
):
    filename = uuid.uuid4().hex
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    
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
        logger.warning("Failed to encode image to WebP %s", exc)
        return None
    
    output.seek(0)
        
    name = os.path.splitext(filename)[0]
    new_name = f"{name}.webp"
    return ContentFile(output.read(), name=new_name)

    

def download_image(url: str, timeout: int=20)-> bytes|None:
    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={
                "User-Agent": "Mozilla/5.0",
            }
        )
        response.raise_for_status()
        
        return response.content
    except Exception as exc:
        logger.warning(
            "Failed to download from %s: %s",
            url,
            exc
        )
        return None
    
def image_byte_to_webp(
    image_bytes: bytes,
    quality=85,
    max_size=None,
):
    try:
        img = Image.open(
            io.BytesIO(image_bytes)
        )
        
        return _image_to_webp(
            img,
            quality,
            max_size,
        )
    
    except (UnidentifiedImageError,OSError,) as exc:
        logger.warning("Failed to open downloaded image bytes %s", exc)
        return None
        
    
def download_and_convert_webp(
    url: str,
    quality=85,
    max_size=None,
):
    image_bytes = download_image(url)
    
    if not image_bytes:
        return None
    
    return image_byte_to_webp(
        image_bytes,
        quality,
        max_size,
    )

###
def save_remote_image_to_field(
    instance,
    field_name: str,
    url: str,
    max_size=None,
):
    webp = download_and_convert_webp(
        url,
        max_size=max_size
    )
    
    if not webp:
        return False
    
    field = getattr(instance, field_name, None)
    
    if field is None:
        raise ValueError(
            f"{instance.__class__.__name__} has no field '{field_name}'"
        )
    
    field.save(
        webp.name,
        webp,
        save=False
    )
    
    return True
    
    
    