import uuid
from operator import attrgetter
from pathlib import Path
from django.utils.deconstruct import deconstructible

@deconstructible
class UploadToPath:
    """Generate a upload path with an SEO-friendly filename.
 
    Filename format: ``<slug>-<8-char-uuid><ext>``
 
    Args:
        base_path:  Top-level folder, e.g. ``'cars'``.
        sub_path:   Optional sub-folder, e.g. ``'gallery'``.
        slug_field: Dotted attribute path on the instance used to build the
                    slug part of the filename.  Supports traversal, so you
                    can pass ``'car.slug'`` for a ``CarImage`` instance.
                    Defaults to ``'slug'``.
 
    Examples::
 
        # Brand logo  →  brand/logos/toyota-3f9a1b2c.webp
        UploadToPath('brand', 'logos', slug_field='slug')
 
        # CarModel thumbnail  →  cars/thumbnail/toyota-camry-4e8d2a1f.webp
        UploadToPath('cars', 'thumbnail', slug_field='slug')
 
        # CarImage (slug lives on the related variant)
        #   →  cars/gallery/toyota-camry-v6-7c3b9e4a.webp
        UploadToPath('cars', 'gallery', slug_field='car.slug')
    """
    def __init__(self, base_path, sub_path: str | None=None, slug_field: str = "slug"):
        self.base_path = base_path
        self.sub_path = sub_path
        self.slug_field = slug_field
        
    def __call__(self, instance, filename):
        ext = Path(filename).suffix.lower()
        short_uuid = uuid.uuid4().hex[-8:]
        
        try:
            slug = attrgetter(self.slug_field)(instance) or ""
        except AttributeError:
            slug = ""
            
        slug = slug[:60] if slug else ""
        base_name = f"{slug}-{short_uuid}" if slug else short_uuid
        
        sub = f"{self.sub_path}/" if self.sub_path else ""

        return f"{self.base_path}/{sub}{base_name}{ext}"
    
    def __eq__(self, other):
        return (
            isinstance(other, UploadToPath)
            and self.base_path == other.base_path
            and self.sub_path == other.sub_path
            and self.slug_field == other.slug_field
        )