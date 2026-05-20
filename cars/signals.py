import logging
from django.db.models.signals import post_delete, pre_save, post_save
from django.dispatch import receiver
from django.db.models import Avg
from django.core.cache import cache

from .models import Brand, CarImage, CarModel, Review, CarVariant
from .utils.image_utils import convert_to_webp
import os

logger = logging.getLogger(__name__)

# Resize uploaded images to at most this dimension before saving as WebP.
# Reduces storage and bandwidth without visible quality loss for web use.
_THUMBNAIL_MAX_SIZE = (1280, 1280)
_GALLERY_MAX_SIZE = (1920, 1920)
_LOGO_MAX_SIZE = (400, 400)
_MODEL_TO_WATCH = [CarModel, Review, Brand, CarVariant]

_WEBP_REGISTRY = [
    # (Model,    field_name,    update_field,  max_size)
    (Brand,    "logo",        "logo",        _LOGO_MAX_SIZE),
    (CarModel, "thumbnail",   "thumbnail",   _THUMBNAIL_MAX_SIZE),
    (CarImage, "image",       "image",       _GALLERY_MAX_SIZE),
]

@receiver([post_save, post_delete], sender=None)
def clear_dashboard_cache(sender, instance, **kwargs):
    if sender in _MODEL_TO_WATCH:
        cache.delete("admin_dashboard_context")

# Helper
def _replace_with_webp(instance, field_name: str, max_size:tuple):
    """Convert the image on *field_name* to WebP and reassign it in-place.

    Returns True if the field was replaced, False otherwise.
    The caller is responsible for saving the instance.
    """
    field = getattr(instance, field_name)
    if not field:
        return False
    
    webp_file = convert_to_webp(field, quality=85, max_size=max_size)
    if webp_file is None:
        logger.warning(
            "_replace_with_webp: conversion failed for %s %s (pk=%s)",
            type(instance).__name__, field_name, instance.pk
            )
        return False
    # Delete the original file from storage before overwriting the field so
    # we don't leave orphaned files behind.
    field.delete(save=False)
    setattr(instance, field_name, webp_file)
    return True
    
def _delete_image_field(instance) -> None:
    """Delete every FileField / ImageField file attached to *instance*."""
    for field in instance._meta.fields:
        if field.get_internal_type() in ('FileField', 'ImageField'):
            file_field = getattr(instance, field.name)
            if file_field and file_field.storage.exists(file_field.name):
                file_field.delete(save=False)
                


@receiver(post_delete, sender=Brand)
@receiver(post_delete, sender=CarModel)
@receiver(post_delete, sender=CarImage)
def delete_image_file(sender, instance, **kwargs):
    _delete_image_field(instance)

@receiver(pre_save, sender=Brand)
def auto_delete_logo_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_logo = Brand.objects.get(pk=instance.pk).logo
    except Brand.DoesNotExist:
        return
    if old_logo and old_logo != instance.logo:
        old_logo.delete(save=False)
        
@receiver(pre_save, sender=CarModel)
def auto_delete_thumbnail_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_image = CarModel.objects.get(pk=instance.pk).thumbnail
    except CarModel.DoesNotExist:
        return
    if old_image and old_image != instance.thumbnail:
        old_image.delete(save=False)

@receiver(pre_save, sender=CarImage)
def auto_delete_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_image = CarImage.objects.get(pk=instance.pk).image
    except CarImage.DoesNotExist:
        return
    if old_image and old_image != instance.image:
        old_image.delete(save=False)

# ---------------------------------------------------------------------------
# Convert uploaded images to WebP on save
#
# We use post_save + update_fields so the converted file is persisted without
# triggering another full save() cycle (and without re-firing pre_save logic).
# ---------------------------------------------------------------------------

def _make_webp_handler(field_name:str, update_field:str, max_size:tuple):
    def handler(sender, instance, **kwargs):
        if kwargs.get("update_field") == frozenset({update_field}):
            return
        if _replace_with_webp(instance, field_name, max_size):
            sender.objects.filter(pk=instance.pk).update(
                **{update_field: getattr(instance, field_name)}
            )
    return handler

for _model, _field_name, _update_field, _max_size in _WEBP_REGISTRY:
    receiver(post_save, sender=_model)(
        _make_webp_handler(_field_name, _update_field, _max_size)
    )
        

        
# ---------------------------------------------------------------------------
# Recompute avg_rating on CarModel when a Review is saved / deleted
# ---------------------------------------------------------------------------

@receiver(post_save, sender=Review)
def update_car_rating_on_save(sender, instance, **kwargs):
    instance.car.recalculate_avg_rating()
    
@receiver(post_delete, sender=Review)
def update_car_rating_on_delete(sender, instance, **kwargs):
    instance.car.recalculate_avg_rating()


