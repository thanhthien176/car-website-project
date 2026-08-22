from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from cars.validators import validate_image_size, validate_image_extension
from cars.utils.upload_utils import UploadToPath
from cars.models import ImageAttributionMixin
from .base import ArticleBase, SectionBase

class BlogCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Blog Categories"
        ordering = ["name"]
        
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
            
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.name
    
    
class BlogTag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Blog Tags"
        ordering = ["name"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
    

class BlogPost(ArticleBase):
    category = models.ForeignKey("BlogCategory", on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    tags = models.ManyToManyField("BlogTag", blank=True, related_name="posts")
    
    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ["-published_at", "-created_at"]
        
        
    def get_absolute_url(self):
        return reverse("blogs:post_detail", kwargs={"slug": self.slug})
    

class BlogSection(ImageAttributionMixin, SectionBase):
    post = models.ForeignKey("BlogPost", on_delete=models.CASCADE, related_name="sections")
    image = models.ImageField(
        upload_to = UploadToPath("blogs", "post_section", slug_field="post.slug"),
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size]
    )
    
    class Meta:
        verbose_name = "Blog Section"
        verbose_name_plural = "Blog Sections"
        ordering = ["order"]
    
    