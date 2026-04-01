from django.db import models
from django.utils.text import slugify
from .validators import validate_image_size, validate_image_extension

# Create your models here.
class Brand(models.Model):
    """Brand: Toyota, Kia, Huynda, Vinfast"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    country_of_origin = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="brand/logos/", blank=True, null=True, validators=[validate_image_size, validate_image_extension])
    description = models.TextField(blank=True)
    founded_year = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        
    def save(self, *args, **kwargs):
        # Automatically generate a slug from name if it doesn't already exit.
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name
    
class Car(models.Model):
    """Specific model: Toyota Camry 2024"""
    BODY_TYPE_CHOICES = [
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('pickup', 'Pickup Truck'),
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('minivan', 'Minivan'),
    ]
    
    FUEL_TYPE_CHOICES = [
        ('gasoline', 'Xăng'),
        ('diesel', 'Diesel'),
        ('electric', 'Điện'),
        ('hybrid', 'Hybrid'),
        ('plug_in_hybrid', 'Plug-in Hybrid'),
    ]
    
    TRANSMISSION_CHOICES = [
        ('automatic', 'Tự động'),
        ('manual', 'Số sàn'),
        ('cvt', 'CVT'),
    ]
    
    # Basic information
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    model_year = models.IntegerField()
    description = models.TextField(blank=True)
    
    # classification
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)    
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    
    # price
    price_min = models.DecimalField(max_digits=15, decimal_places=0)
    price_max = models.DecimalField(max_digits=15, decimal_places=0)
    
    # Basic Specifications
    engine_capacity = models.DecimalField(
        max_digits=4, decimal_places=1,
        null=True, blank=True, 
        help_text='Dung tích xi lanh (lít)'
        )
    horsepower = models.IntegerField(null=True, blank=True, help_text="Mã lực")
    seating_capacity = models.IntegerField(default=5)
    
    # Image    
    thumbnail = models.ImageField(upload_to='cars/thumbnails/', blank=True, null=True, validators=[validate_image_size, validate_image_extension])
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Rating
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, help_text="Automatically updated from reviews") 
    
    class Meta:
        ordering = ['brand', 'name', '-model_year']
        verbose_name = 'Car'
        verbose_name_plural = 'Cars'
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.brand.name}-{self.name}-{self.model_year}')
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.brand} {self.name} {self.model_year}"
    
    @property
    def price_range(self):
        min_m = self.price_min/1_000_000
        max_m = self.price_max/1_000_000
        return f'{min_m:,.0f} - {max_m:,.0f} triệu VNĐ'
    
    @property
    def primary_image(self):
        img = self.images.filter(is_primary=True).first()
        if img:
            return img.image.url
        fallback = self.images.first()
        return fallback.image.url if fallback else None
        
class CarSpecification(models.Model):
    car = models.OneToOneField(Car, on_delete=models.CASCADE, related_name="specification")
    
    # Engine
    engine_type = models.CharField(max_length=100, blank=True)
    displacement = models.PositiveIntegerField(null=True, blank=True, help_text="cc")
    max_power = models.PositiveIntegerField(null=True, blank=True, help_text="Hp")
    max_torque = models.PositiveIntegerField(null=True, blank=True, help_text="Nm")
    
    # Performance
    acceleration_0_100 = models.DecimalField(max_digits=3, decimal_places=1 ,null=True, blank=True, help_text="giây")
    top_speed = models.PositiveIntegerField(null=True, blank=True, help_text="km/h")
    fuel_consumption = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, help_text="L/100km")
    
    # Dimension
    length = models.PositiveIntegerField(null=True, blank=True, help_text="mm")
    width = models.PositiveIntegerField(null=True, blank=True, help_text="mm")
    height = models.PositiveIntegerField(null=True, blank=True, help_text="mm")
    wheelbase = models.PositiveIntegerField(null=True, blank=True, help_text="mm")
    
    # Safety & Features
    safety_rating = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Sao NCAP")
    num_airbags =models.PositiveSmallIntegerField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Specification"
        
    def __str__(self):
        return f"Thông số - {self.car.name}"
    
class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='cars/gallery/%Y/%m', validators=[validate_image_size, validate_image_extension])
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
        
class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} star") for i in range(1,6)]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="reviews")
    author_name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    pros = models.TextField(blank=True, help_text="Ưu điểm")
    cons = models.TextField(blank=True, help_text="Nhược điểm")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Đánh giá'
        verbose_name_plural = 'Reviews'
        
    def __str__(self):
        return f"{self.author_name} - {self.car.name} ({self.rating}*)"
    
    
    
    