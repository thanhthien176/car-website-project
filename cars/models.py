from django.db import models
from django.db.models import Avg
from django.utils.text import slugify
from .validators import validate_image_size, validate_image_extension
from .utils.upload_utils import UploadToPath

# Create your models here.
class SEOMetaData(models.Model):
    seo_title = models.CharField(max_length=70, blank=True, help_text="Tiêu đề hiển thị kết quả tìm kiếm(tối ưu <70 ký tự)")
    seo_description = models.CharField(max_length=160, blank=True, help_text="Mô tả ngắn gọn về trang(tối ưu: 150-160 ký tự)")
    seo_keyword = models.CharField(max_length=255, blank=True, help_text="Các từ khóa cách nhau bằng dấu phẩy")
    
    class Meta:
        abstract = True
        
class BodyType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
class CarClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name    

class Brand(SEOMetaData, models.Model):
    """Brand: Toyota, Kia, Huynda, Vinfast"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    country_of_origin = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=UploadToPath('brand','logos', slug_field='slug'), 
                             blank=True, null=True, 
                             validators=[validate_image_size, validate_image_extension])
    description = models.TextField(blank=True, null=True)
    founded_year = models.IntegerField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
    
    @property
    def get_seo_title(self):
        return self.seo_title or f"Tìm hiểu các dòng xe của hãng {self.name} | WebsiteCar"
    
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
    
class CarModel(SEOMetaData, models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="car_models")
    name = models.CharField(max_length=100)
    
    body_type = models.ForeignKey(BodyType, on_delete=models.SET_NULL, null=True)
    car_class = models.ForeignKey(CarClass, on_delete=models.SET_NULL, null=True, blank=True)
    
    slug = models.SlugField(unique=True, blank=True)
    
    model_year = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    thumbnail = models.ImageField(upload_to = UploadToPath('cars','thumbnail', slug_field='slug'), 
                                  blank=True, null=True, 
                                  validators=[validate_image_size, validate_image_extension])
    
    avg_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['brand','name'],
                name="unique_brand_name"
            )
        ]
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['brand'])
        ]
        ordering = ['brand__name','name', '-model_year']
        verbose_name_plural = "Car Models"
    
    @property
    def get_seo_title(self):
        return (
            self.seo_title 
            or f"Tìm hiểu mẫu xe {self.name} của hãng {self.brand.name} | WebsiteCar"
            )
    
    @property
    def get_seo_description(self):
        return (
            self.seo_description 
            or f"Thông tin chi tiết, thông số kỹ thuật, giá bán của"
            f"{self.brand.name}-{self.name}"
            )
        
    def recalculate_avg_rating(self)-> None:
        avg = self.reviews.filter(is_approved=True).aggregate(Avg("rating"))["rating__avg"]
        self.avg_rating = avg or 0
        self.save(update_fields=["avg_rating"])
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.brand.name}-{self.name}")
            
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.brand.name} {self.name}"
    
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
    
    FUEL_TYPE_CHOICES = [
        ('gasoline', 'Xăng'),
        ('diesel', 'Diesel'),
        ('electric', 'Điện'),
        ('hybrid', 'Hybrid'),
        ('phev', 'Plug-in Hybrid'),
    ]

    
    # Basic Information
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="variants")
    variant_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    
    # classification
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)    
    
    # price
    price_min = models.DecimalField(max_digits=15, decimal_places=0)
    price_max = models.DecimalField(max_digits=15, decimal_places=0)
    
    is_active = models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['car_model', 'variant_name'],
                name="unique_car_variant"
            )
        ]
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['fuel_type'])
        ]
        verbose_name = "Variant"
        verbose_name_plural = "Variants"
        
    def get_meta_title(self):
        return (self.seo_title 
                or f"Giá xe {self.car_model} {self.variant_name} mới nhất"
                f"| WebsiteCar"
        )
    
    def get_meta_description(self):
        if self.seo_description:
            return self.seo_description
        
        return (
            f"Đánh giá {self.variant_name}, động cơ {self.fuel_type},"
            f"giá từ {self.price_range}. Xem chi tiết thông số kỹ thuật tại đây."
            )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.car_model}-{self.variant_name}")
        super().save(*args, **kwargs)
        
    @property
    def price_range(self):
        if self.price_min is None or self.price_max is None:
            return "Liên hệ"
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
        
    def __str__(self):
        return f"{self.car_model} {self.variant_name}"
    
class DimensionSpecification(models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='dimension')
    
    length = models.PositiveIntegerField(null=True, blank=True, help_text="Chiều dài(mm)")
    width = models.PositiveIntegerField(null=True, blank=True, help_text="Chiều rộng(mm)")
    height = models.PositiveIntegerField(null=True, blank=True, help_text="chiều cao(mm)")
    
    wheelbase = models.PositiveIntegerField(null=True, blank=True, help_text="Chiều dài cơ sở(mm)")
    ground_clearance = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Khoảng sáng gầm xe(mm)")
        
    seating_capacity = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Số chỗ ngồi")
    fuel_tank_capacity = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Dung tích bình nhiên liệu(lít)")
    
class EngineSpecification(models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Tự động'),
        ('manual', 'Số sàn'),
        ('cvt', 'CVT'),
    ]
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='engine')
    
     # Engine - performance
    engine_type = models.CharField(max_length=100, blank=True)
    displacement = models.PositiveIntegerField(null=True, blank=True, help_text="Dung tích xi lanh(cc)")
    max_power = models.PositiveIntegerField(null=True, blank=True, help_text="Công suất tối đa(Hp)")
    max_torque = models.PositiveIntegerField(null=True, blank=True, help_text="Momen xoắn tối đa(Nm)")
    drive_train = models.CharField(max_length=30, null=True, blank=True, help_text="Hệ số truyền động")
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)

class PerformanceSpecification(models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='performance')
    
    # suspension
    suspension_font = models.CharField(max_length=30, null=True, blank=True, help_text="Hệ thống treo trước")
    suspension_rear = models.CharField(max_length=30, null=True, blank=True, help_text="Hệ thống treo sau")
    
    # Tire & wheel
    tire_size = models.CharField(max_length=30, null=True, blank=True, help_text="Kích thước lốp xe")
    brake = models.CharField(max_length=30, null=True, blank=True, help_text="Phanh trước/sau(front/rear)")
    
    
class FuelConsumptionSpecification(models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='fuel_consumption')
    
    # fuel comsumption
    urban = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Trong đô thị(lit/100km)")
    extra_urban = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Ngoài đô thị(lít/100km)")
    combined = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Kết hợp(lít/100km)")
    
class ExteriorSpecification(models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='exterior')
    
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
    
class InteriorSpecification(models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='interior')
    
    # Interior
    steering_type = models.CharField(max_length=30, null=True, blank=True, help_text="Loại tay lái")
    steering_material = models.CharField(max_length=30, null=True, blank=True, help_text="Chất liệu tay lái")
    steering_adjust = models.CharField(max_length=30, null=True, blank=True, help_text="Điều chỉnh tay lái")
    paddle_shifter = models.BooleanField(default=False, help_text="Lẫy chuyển số")
    inner_mirror = models.CharField(max_length=50, null=True, blank=True, help_text="Gương chiếu hậu trong")
    combination_metter = models.CharField(max_length=50, null=True, blank=True, help_text="Cụm đồng hồ")
    sunroof = models.CharField(max_length=30, null=True, blank=True, help_text="Cửa sổ trời")
    
class SeatSpecification(models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='seat')
    
    # Seat
    seat_material = models.CharField(max_length=30, null=True, blank=True, help_text="Chất liệu bọc ghế")
    driver_seat = models.CharField(max_length=30, null=True, blank=True, help_text="Điều chỉnh ghế lái")
    front_passeger_seat = models.CharField(max_length=30, null=True, blank=True, help_text="Điều chỉnh ghế hành khách")
    rear_seat = models.CharField(max_length=30, null=True, blank=True, help_text="Ghế sau")
    
class ComfortSpecification(models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='comfort')
    
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
    
class SafetySpecification(models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='safety')
    
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
    
    safety_rating = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Sao NCAP")
    
    
class CarImage(models.Model):
    car = models.ForeignKey(CarVariant, on_delete=models.CASCADE, related_name="images")
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
        
class Review(models.Model):
    RATING_CHOICES = [(i, f"{i} star") for i in range(1,6)]
    
    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="reviews")
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
        verbose_name_plural = 'Đánh giá'
        
    def __str__(self):
        return f"{self.author_name} - {self.car} ({self.rating}*)"
    

class Comparison(models.Model):
    session_key = models.CharField(max_length=40, blank=True)
    cars = models.ManyToManyField(CarVariant, related_name='comparisons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Car Comparison"
    
    def __str__(self):
        car_names = ", ".join(car.variant_name for car in self.cars.all()) 
        return f"So sánh: {car_names or "Chưa có xe"}"
    
    def can_add_car(self):
        # Maximum of 3 vehicles per comparison.
        return self.cars.count() < 3
    


    
    