from django.db import models
from django.utils.text import slugify
from .validators import validate_image_size, validate_image_extension
from .utils import UploadToPath

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
    
class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="car_models")
    name = models.CharField(max_length=100,)
    car_slug = models.SlugField(max_length=200, unique=True, blank=True)
    model_year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    thumnail = models.ImageField(upload_to = UploadToPath("thumnail"), blank=True, null=True, validators=[validate_image_size, validate_image_extension])
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['brand','name'],
                name="unique_brand_name"
            )
        ]
        ordering = ['brand__name','name', '-model_year']
        verbose_name_plural = "Car Models"
        
    def save(self, *args, **kwargs):
        if not self.car_slug:
            base_slug = slugify(f"{self.brand.name}-{self.name}-{self.model_year}")
            
            slug = base_slug
            counter = 1
            
            while CarModel.objects.filter(car_slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.car_slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.brand.name} {self.name}"
    
class CarVariant(models.Model):
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

    
    # Basic Information
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="variants")
    variant_name = models.CharField(max_length=100)
    variant_slug = models.SlugField(max_length=300, unique=True, blank=True)
    
    # classification
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)    
    
    # price
    price_min = models.DecimalField(max_digits=15, decimal_places=0)
    price_max = models.DecimalField(max_digits=15, decimal_places=0)
    
    # Dimension - weight
    length = models.PositiveIntegerField(null=True, blank=True, help_text="Chiều dài(mm)")
    width = models.PositiveIntegerField(null=True, blank=True, help_text="Chiều rộng(mm)")
    height = models.PositiveIntegerField(null=True, blank=True, help_text="chiều cao(mm)")
    wheelbase = models.PositiveIntegerField(null=True, blank=True, help_text="Chiều dài cơ sở(mm)")
    ground_clearance = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Khoảng sáng gầm xe(mm)")
    seating_capacity = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Số chỗ ngồi")
    fuel_tank_capacity = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Dung tích bình nhiên liệu(lít)")


    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['car_model', 'variant_name'],
                name="unique_car_variant"
            )
        ]
        verbose_name = "Variant"
        verbose_name_plural = "Variants"
    
    def save(self, *args, **kwargs):
        if not self.variant_slug:
            base_slug = slugify(f"{self.car_model}-{self.variant_name}")
        
            slug = base_slug
            count = 1
            
            while CarVariant.objects.filter(variant_slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            
            self.variant_slug=slug
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.car_model} {self.variant_name}"
    
class VariantSpecification(models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Tự động'),
        ('manual', 'Số sàn'),
        ('cvt', 'CVT'),
    ]
     
    DRIVE_MODE_CHOICES = [
        ('Power', 'Công suất cao'),
        ('Eco', 'Tiết kiệm nhiên liệu'),
        ('Normal', 'Thông thường')
    ]
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name="specification")
    
     # Engine - performance
    engine_type = models.CharField(max_length=100, blank=True)
    displacement = models.PositiveIntegerField(null=True, blank=True, help_text="Dung tích xi lanh(cc)")
    max_power = models.PositiveIntegerField(null=True, blank=True, help_text="Công suất tối đa(Hp)")
    max_torque = models.PositiveIntegerField(null=True, blank=True, help_text="Momen xoắn tối đa(Nm)")
    drive_mode = models.CharField(max_length=30, choices=DRIVE_MODE_CHOICES, null=True, blank=True)
    drive_train = models.CharField(max_length=30, null=True, blank=True, help_text="Hệ số truyền động")
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    
    # suspension
    suspension_font = models.CharField(max_length=30, null=True, blank=True, help_text="Hệ thống treo trước")
    suspension_rear = models.CharField(max_length=30, null=True, blank=True, help_text="Hệ thống treo sau")
    
    # Tire & wheel
    tire_size = models.CharField(max_length=30, null=True, blank=True, help_text="Kích thước lốp xe")
    
    brake = models.CharField(max_length=30, null=True, blank=True, help_text="Phanh trước/sau(front/rear)")
    
    # fuel comsumption
    urban_comsumption = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Trong đô thị(lit/100km)")
    ex_urban_comsumption = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Ngoài đô thị(lít/100km)")
    combine_comsumption = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Kết hợp(lít/100km)")
    
    # exterior
    headlamp = models.CharField(max_length=30, null=True, blank=True, help_text="Đèn chiếu sáng trước")
    daytime_running_light = models.BooleanField(default=False)
    auto_light_control = models.BooleanField(default=False)
    rearlamp = models.CharField(max_length=30, null=True, blank=True, help_text="Đèn hậu")
    foglamp = models.CharField(max_length=30, null=True, blank=True, help_text="Đèn sương mù")
    
    # Outer mirrors
    power_fold_mirror = models.BooleanField(default=False)
    power_adjust_mirror = models.BooleanField(default=False)
    turn_signal_lamp = models.BooleanField(default=False, help_text="Tích hợp đèn báo rẽ")
    
    # wiper
    wiper_front = models.CharField(max_length=30, null=True, blank=True, help_text="Gạt mưa trước")
    wiper_rear = models.CharField(max_length=30, null=True, blank=True, help_text="Gạt mưa sau")
    rear_glass_defrogger = models.BooleanField(default=False, help_text="Chức năng sấy kính sau")
    
    # Interior
    steering_type = models.CharField(max_length=30, null=True, blank=True, help_text="Loại tay lái")
    steering_material = models.CharField(max_length=30, null=True, blank=True, help_text="Chất liệu tay lái")
    steering_adjust = models.CharField(max_length=30, null=True, blank=True, help_text="Điều chỉnh tay lái")
    paddle_shifter = models.BooleanField(default=False, help_text="Lẫy chuyển số")
    inner_mirror = models.CharField(max_length=50, null=True, blank=True, help_text="Gương chiếu hậu trong")
    combination_metter = models.CharField(max_length=50, null=True, blank=True, help_text="Cụm đồng hồ")
    sunroof = models.CharField(max_length=30, null=True, blank=True, help_text="Cửa sổ trời")
    
    # Seat
    seat_material = models.CharField(max_length=30, null=True, blank=True, help_text="Chất liệu bọc ghế")
    driver_seat = models.CharField(max_length=30, null=True, blank=True, help_text="Điều chỉnh ghế lái")
    front_passeger_seat = models.CharField(max_length=30, null=True, blank=True, help_text="Điều chỉnh ghế hành khách")
    rear_seat = models.CharField(max_length=30, null=True, blank=True, help_text="Ghế sau")
    
    # Utilities & Comfort
    air_conditioner = models.CharField(max_length=20, null=True, blank=True, help_text="Hệ thống điều hòa")
    rear_air_duct = models.BooleanField(default=False, help_text="Cửa gió sau")
    display = models.CharField(max_length=30, null=True, blank=True, help_text="Màn hình giải trí")
    number_of_speaker = models.CharField(max_length=30, null=True, blank=True, help_text="Số loa")
    smart_connect = models.CharField(max_length=30, null=True, blank=True, help_text="Kết nối không dây")
    smart_key = models.BooleanField(default=False, help_text="Chìa khóa thông minh")
    power_window = models.CharField(max_length=30, null=True, blank=True, help_text="Cửa sổ điều chỉnh điện")
    power_back_door = models.BooleanField(default=False, help_text="Cốp điện")
    cruise_control = models.BooleanField(default=False, help_text="Hệ thống điều khiển hành trình")
    electric_parking_brake = models.BooleanField(default=False, help_text="Phanh tay điện tủ")
    brake_hold = models.BooleanField(default=False, help_text="Giữ phanh tự động")
    
    # active safety
    pcs = models.BooleanField(default=False, help_text="Cảnh báo tiền va chạm(pre-collision warning)")
    lda = models.BooleanField(default=False, help_text="Cảnh báo lệch làn đường(Lane departure alert")
    lta = models.BooleanField(default=False, help_text="Hỗ trợ giữ làn đường(lane tracing assist")
    drcc = models.BooleanField(default=False, help_text="Hệ thống điều khiển hành trình chủ động(Dynamic radar cruise control)")
    ahb = models.BooleanField(default=False, help_text="Đèn chiếu xa tự động(Automatic high beam)")
    parking_camera = models.CharField(max_length=30, null=True, blank=True, help_text="camera hỗ trợ đỗ xe")
    bsm = models.BooleanField(default=False, help_text="Hế thống cảnh báo điểm mù(Blind spot monitor)")
    rcta = models.BooleanField(default=False, help_text="Hệ thống hỗ trợ phương tiện cắt ngang phía sau(Rear cross traffic alert)")
    abs = models.BooleanField(default=False, help_text="Hệ thống chống bó cứng phanh(Anti-lock braking system)")
    ba = models.BooleanField(default=False, help_text="Hệ thống hỗ trợ lực phanh khẩn cấp(Brake assist)")
    ebd = models.BooleanField(default=False, help_text="Hệ thống phân phối lực phanh điện từ(Electronic brake-force distribution)")
    vsc = models.BooleanField(default=False, help_text="Hệ thống cân bằng điện tử(vehicle stability control")
    trc = models.BooleanField(default=False, help_text="Hệ thống kiểm soát lực kéo(Traction control")
    hac = models.BooleanField(default=False, help_text="Hệ thống hỗ trợ khởi hành ngang dốc(Hill-start assist control")
    ebs = models.BooleanField(default=False, help_text="Hệ thống phanh khẩn cấp(Emergency brake signal)")
    tpws = models.BooleanField(default=False, help_text="Hệ thống cảnh báo áp suất lốp(Tyre pressure warning system)")
    sensor = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Cảm biến hỗ trợ đổ xe")
    airbag = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Túi khí")
    
    def __str__(self):
        return f"Thông số - {self.variant}"
    
  
    
    
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
    
    DRIVE_MODE = [
        ('')
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
    

class Comparison(models.Model):
    session_key = models.CharField(max_length=40, blank=True)
    cars = models.ManyToManyField(Car, related_name='comparisons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Car Comparison"
    
    def __str__(self):
        car_names = ", ".join([car.name for car in self.cars.all()]) 
        return f"So sánh: {car_names or "Chưa có xe"}"
    
    def can_add_car(self):
        # Maximum of 3 vehicles per comparison.
        return self.cars.count() < 3
    
    
    