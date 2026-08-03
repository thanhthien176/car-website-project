from django.db import models

from .car_models import CarModel, CarVariant
from cars.utils.upload_utils import UploadToPath
from cars.validators import validate_image_size, validate_image_extension


class CarImage(models.Model):
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=UploadToPath('cars', 'gallery', slug_field='car.slug'), 
                              validators=[validate_image_size, validate_image_extension])
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Car picture"
        
    def save(self, *args, **kwargs):
        if self.is_primary:
            CarImage.objects.filter(
                car = self.car, is_primary = True
            ).exclude(pk=self.pk).update(is_primary = False)
        
        super().save(*args, **kwargs)
        
class VariantImage(models.Model):
    variant = models.ForeignKey(CarVariant, on_delete=models.CASCADE, related_name='variant_images')
    image = models.ImageField(upload_to=UploadToPath('variants','gallery', slug_field='variant.slug'),
                              validators=[validate_image_extension, validate_image_size], blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Variant picture'
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            VariantImage.objects.filter(
                variant = self.variant, is_primary = True
            ).exclude(pk=self.pk).update(is_primary = False)
        
        super().save(*args, **kwargs)