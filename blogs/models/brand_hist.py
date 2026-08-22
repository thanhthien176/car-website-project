from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from cars.utils.upload_utils import UploadToPath
from cars.validators import validate_image_size, validate_image_extension
from cars.models import ImageAttributionMixin
from .base import ArticleBase, SectionBase


class BrandHistory(ArticleBase):
    brand = models.OneToOneField("cars.Brand", on_delete=models.CASCADE, related_name="history")
    
    class Meta:
        verbose_name = "Brand History"
        verbose_name_plural = "Brand Histories"
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand}-history")       
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("cars:brand_history", kwargs={"slug": self.brand.slug})
    
    
class BrandHistorySection(ImageAttributionMixin, SectionBase):
    history = models.ForeignKey(
        "BrandHistory", on_delete=models.CASCADE, related_name="sections"
    )
    image = models.ImageField(
        upload_to = UploadToPath("blogs", "brand_history_sections", slug_field="history.brand.slug"),
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size]
    )
    
    class Meta:
        ordering = ["order"]
        verbose_name = "Brand History Section"
    
    

