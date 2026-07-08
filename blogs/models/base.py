from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class ArticleBase(models.Model):
    """
        Shared metadata for any long-form content: BlogPost, CarDescription,
        BrandHistory. Deliberately holds no content field — actual body text
        lives in the corresponding SectionBase subclass, one-to-many.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_articles"   #  %(class)s avoids related_name clashes across BlogPost/CarDescription/BrandHistory, all of which inherit this same abstract field.
    )
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        ordering = ["-published_at", "-created_at"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.is_published and self.published_at is None:
            self.published_at = timezone.now()
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    

class SectionBase(models.Model):
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    
    class Meta:
        abstract = True
        ordering = ["order"]
        
    def __str__(self) -> str:
        return self.title or f"Section #{self.order}"
    