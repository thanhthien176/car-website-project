from django.db.models.signals import post_delete, pre_save, post_delete, post_save
from django.dispatch import receiver
from django.db.models import Avg
from .models import CarImage, Brand, Car, Review
import os

@receiver(post_delete, sender=Brand)
@receiver(post_delete, sender=Car)
@receiver(post_delete, sender=CarImage)
def delete_image_file(sender, instance, **kwargs):
    
    for field in instance._meta.fields:
        if field.get_internal_type() in ['FileField', 'ImageField']:
            file_field = getattr(instance, field.name)
            if file_field and file_field.storage.exists(file_field.name):
                file_field.delete(save=False)

@receiver(pre_save, sender=Brand)
def auto_delete_logo_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_image = Brand.objects.get(pk=instance.pk).logo
    except Brand.DoesNotExist:
        return
    if old_image and old_image != instance.logo:
        old_image.delete(save=False)
        
@receiver(pre_save, sender=Car)
def auto_delete_thumbnail_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_image = Car.objects.get(pk=instance.pk).thumbnail
    except Car.DoesNotExist:
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
        

@receiver(post_save, sender=Review)
def update_car_rating_on_save(sender, instance, **kwargs):
    _recalculate_rating(instance.car)
    
@receiver(post_delete, sender=Review)
def update_car_rating_on_delete(sender, instance, **kwargs):
    _recalculate_rating(instance.car)    
    

def _recalculate_rating(car):
    avg = car.reviews.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg']
    car.avg_rating = avg or 0
    car.save(update_fields = ['avg_rating'])

