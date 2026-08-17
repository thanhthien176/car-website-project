from decimal import Decimal
from typing import TYPE_CHECKING

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse

from cars.validators import validate_image_size, validate_image_extension
from cars.utils.upload_utils import UploadToPath



# SEOMetaDat
class SEOMetaData(models.Model):
    seo_title = models.CharField(max_length=70, blank=True, help_text="Tiêu đề hiển thị kết quả tìm kiếm(tối ưu <70 ký tự)")
    seo_description = models.CharField(max_length=160, blank=True, help_text="Mô tả ngắn gọn về trang(tối ưu: 150-160 ký tự)")
    seo_keyword = models.CharField(max_length=255, blank=True, help_text="Các từ khóa cách nhau bằng dấu phẩy")
    
    class Meta:
        abstract = True
        

# Bodytype       
class BodyType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural= "Body Types"
    
    def __str__(self):
        return self.name

# CarClass
class CarClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Car Classes"
    
    def __str__(self):
        return self.name 
   

# Brand
class Brand(SEOMetaData, models.Model):
    """Brand: Toyota, Kia, Huynda, Vinfast"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    country_of_origin = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=UploadToPath('brand','logos', slug_field='slug'), 
                             blank=True, null=True, 
                             validators=[validate_image_size, validate_image_extension])
    description = models.TextField(blank=True)
    founded_year = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    display_order = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], help_text="Ưu tiên xuất hiện")
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
    
    @property
    def get_seo_title(self):
        return self.seo_title or f"Tìm hiểu các dòng xe của hãng {self.name} | Xehoi360.com.vn"
    
    @property
    def get_seo_description(self):
        return self.seo_description or f"Tìm hiểu các dòng xe của hãng {self.name} đến từ {self.country_of_origin}. Cập nhật thông số  và giá bán"
        
    def save(self, *args, **kwargs):
        # Automatically generate a slug from name if it doesn't already exit.
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("cars:brand_detail", kwargs={"slug": self.slug})
    

# Car Model
class CarModel(SEOMetaData, models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="car_models")
    name = models.CharField(max_length=100)
    
    body_type = models.ForeignKey(BodyType, on_delete=models.SET_NULL, null=True)
    car_class = models.ForeignKey(CarClass, on_delete=models.SET_NULL, null=True, blank=True)
    
    slug = models.SlugField(unique=True, blank=True)
    
    model_year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True)
    
    thumbnail = models.ImageField(upload_to = UploadToPath('cars','thumbnail', slug_field='slug'), 
                                  blank=True, null=True, 
                                  validators=[validate_image_size, validate_image_extension])
    
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    display_order = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)], help_text="Chỉ số để ưu tiên hiển thị")
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['brand','name'],
                name="unique_brand_name"
            )
        ]
        indexes = [
            models.Index(fields=['avg_rating'])
        ]
        ordering = ['brand__name','name', '-model_year']
        verbose_name_plural = "Car Models"
    
    @property
    def get_seo_title(self):
        return (
            self.seo_title 
            or f"Tìm hiểu mẫu xe {self.name} của hãng {self.brand.name} | Xehoi360.com.vn"
            )
    
    @property
    def get_seo_description(self):
        return (
            self.seo_description 
            or f"Thông tin chi tiết, thông số kỹ thuật, giá bán của "
            f"{self.brand.name} {self.name}"
            )
        
    def recalculate_avg_rating(self)-> None:
        avg = self.reviews.filter(is_approved=True).aggregate(Avg("rating"))["rating__avg"] # pyright: ignore[reportAttributeAccessIssue]
        self.avg_rating = avg or 0
        self.save(update_fields=["avg_rating"])
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand.name}-{self.name}")
        super().save(*args, **kwargs)
            
    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first() # type: ignore
        if img:
            return img.image.url
        fallback = self.images.first() # type: ignore
        if fallback:
            return fallback.image.url
        return None
            
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.brand.name} {self.name}"
    
    def get_absolute_url(self):
        return reverse("cars:car_detail", kwargs={"slug": self.slug})
    


class CarVariant(SEOMetaData, models.Model):
    # BODY_TYPE_CHOICES = [
    #     ('sedan', 'Sedan'),
    #     ('suv', 'SUV'),
    #     ('hatchback', 'Hatchback'),
    #     ('pickup', 'Pickup Truck'),
    #     ('coupe', 'Coupe'),
    #     ('convertible', 'Convertible'),
    #     ('minivan', 'Minivan'),
    # ]
    from cars.services import VariantManager
    
    FUEL_TYPE_CHOICES = [
        ('gasoline', 'Xăng'),
        ('diesel', 'Diesel'),
        ('electric', 'Điện'),
        ('hybrid', 'Hybrid'),
        ('phev', 'Plug-in Hybrid'),
    ]

    
    # Basic Information
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="variants")
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    
    # Change
    @property
    def variant_name(self):
        return self.name
    
    # classification
    fuel_system = models.CharField(max_length=100, blank=True, help_text="Hệ thống nhiên liệu")
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)    
    
    # price
    price_min = models.DecimalField(max_digits=15, decimal_places=0)
    price_max = models.DecimalField(max_digits=15, decimal_places=0)
    
    is_active = models.BooleanField(default=True)
    
    origin_country = models.CharField(max_length=100, blank=True, help_text="Xuất xứ")
    number_of_seats = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Số chỗ ngồi")
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # objects = models.Manager.from_queryset(VariantQuerySet)()
    objects: VariantManager = VariantManager()
          
    if TYPE_CHECKING:
        is_saved: bool
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['car_model', 'name'],
                name="unique_car_variant"
            )
        ]
        indexes = [
            models.Index(fields=['fuel_type']),
            models.Index(fields=['price_min'])
        ]
        verbose_name = "Variant"
        verbose_name_plural = "Variants"
        
    def get_meta_title(self):
        return (self.seo_title 
                or f"Giá xe {self.car_model} {self.name} mới nhất"
                f"| Xehoi360.com.vn"
        )
    
    def get_meta_description(self):
        if self.seo_description:
            return self.seo_description
        
        return (
            f"Đánh giá {self.name}, động cơ {self.fuel_type}, "
            f"giá từ {self.price_range}. Xem chi tiết thông số kỹ thuật tại đây."
            )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.car_model}-{self.name}")
            new_slug = base_slug
            count = 1
            while CarVariant.objects.filter(slug=new_slug).exists():
                new_slug = slugify(f"{base_slug}-{count}")
                count += 1
            self.slug = new_slug
            
        super().save(*args, **kwargs)
        
    @property
    def price_range(self):
        if self.price_min is None or self.price_max is None:
            return "Liên hệ"
        min_m = self.price_min/Decimal(1_000_000)
        max_m = self.price_max/Decimal(1_000_000)
        return f'{min_m:,.0f} - {max_m:,.0f} triệu VNĐ'
    
    @property
    def primary_image(self):
        """Return URL of primary (or first) VariantImage. Falls back to the
        parent CarModel's primary_image if this variant has no images of
        its own (e.g. a new variant added before photos were uploaded)."""
        img = self.variant_images.filter(is_primary=True).first() # type: ignore
        if img:
            return img.image.url
        fallback = self.variant_images.first() # type: ignore
        if fallback:
            return fallback.image.url
        return self.car_model.primary_image
        
    def __str__(self):
        return f"{self.car_model} {self.name}"
    
    def get_absolute_url(self):
        return reverse("cars:variant_detail", kwargs={"slug": self.slug})
            
