from django.db import models
from django.utils.text import slugify
from django.urls import reverse

from cars.utils.upload_utils import UploadToPath
from cars.validators import validate_image_size, validate_image_extension




from .base import ArticleBase, SectionBase


class CarDescription(ArticleBase):
    car_model = models.ForeignKey("cars.CarModel", on_delete=models.CASCADE, related_name="descriptions")
    variant = models.ForeignKey("cars.CarVariant", 
                                on_delete=models.CASCADE,
                                related_name="descriptions",
                                null=True,
                                blank=True,
                                help_text="Để trống nếu bài viết dùng chung cho mọi phiên bản của dòng xe này"
                                )
    is_primary = models.BooleanField(
        default=False,
        help_text="Bài chính trong nhóm (theo variant cụ thể, hoặc nhóm dùng chung nếu variant trống)"
    )
    
    class Meta:
        verbose_name = "Car Description"
        verbose_name_plural = "Car Descriptions"
        ordering = ["-is_primary", "-published_at"]
        
    @property
    def image_slug(self):
        """Used by section image upload paths — falls back to the shared
        car_model slug when this description has no specific variant."""
        return self.variant.slug if self.variant else self.car_model.slug
    
    def save(self, *args, **kwargs):
        if not self.slug:
            target = self.variant or self.car_model
            self.slug = slugify(f"{target}-{self.title}")
            
        if self.is_primary:
            # Scope the "only one primary" rule to this exact (car_model,
            # variant) pair — the variant-specific group and the shared
            # (variant=None) group each get their own single primary.
            CarDescription.objects.filter(
                car_model=self.car_model,
                variant=self.variant,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
            
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        if self.variant:
            return reverse("cars:variant_detail", kwargs={"slug": self.variant.slug})
        return reverse("cars:car_detail", kwargs={"slug": self.car_model.slug})
    
class CarDescriptionSection(SectionBase):
    description = models.ForeignKey(
        "CarDescription", on_delete=models.CASCADE, related_name="sections"
    )
    image = models.ImageField(
        upload_to = UploadToPath("blogs", "car_description_sections", slug_field="description.image_slug"),
        blank=True,
        null=True,
        validators=[validate_image_size, validate_image_extension]
    )
    
    class Meta:
        ordering = ["order"]
        verbose_name = "Car Description Section"
    
    

        
        
        

