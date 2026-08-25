from django.db import models
from django.utils.html import format_html
from requests import auth

from .car_models import CarModel, CarVariant
from cars.utils.upload_utils import UploadToPath
from cars.validators import validate_image_size, validate_image_extension

class ImageAttributionMixin(models.Model):
    """
    Abstract Model contains image source information and shared helper methods.
    """
    author_name = models.CharField(max_length=200, blank=True, default="")
    author_url = models.URLField(max_length=500, blank=True, default="")
    source_name = models.CharField(max_length=200, blank=True, default="")
    source_url = models.URLField(max_length=500, blank=True, default="")
    license = models.CharField(max_length=200, blank=True, default="")
    
    class Meta:
        abstract = True
        
    @property
    def attribution_html(self):
        if not any([self.author_name, self.source_name, self.license]):
            return ""

        link_cls = 'class="img-attribution-link"'

        if self.author_name and self.author_url:
            author_part = format_html(
                '''
                <div>
                    <span>Author: </span>
                    <a href="{}" target="_blank" rel="noopener" {}>{}</a>
                </div>
                ''', 
                self.author_url, link_cls, self.author_name)
        else:
            author_part = self.author_name

        if self.source_name and self.source_url:
            source_part = format_html(
                '''
                <div>
                <span>Source: </span>
                <a href="{}" target="_blank" rel="noopener" {}>{}</a>
                </div>
                ''', 
                self.source_url, link_cls, self.source_name)
        else:
            source_part = self.source_name

        if author_part and source_part:
            by_part = format_html('{}  {}', author_part, source_part)
        elif author_part:
            by_part = format_html('{}', author_part)
        elif source_part:
            by_part = format_html('{}', source_part)
        else:
            by_part = ""

        license_part = format_html('<p><span>License: </span> ({})</p>', self.license) if self.license else ""

        return format_html(
            '<figcaption class="img-attribution-text">{}{}</figcaption>',
            by_part,
            license_part
        )
class CarImage(ImageAttributionMixin):
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
        
class VariantImage(ImageAttributionMixin):
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