import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.text import slugify

from cars import validators
from cars.utils.upload_utils import UploadToPath
from cars.validators import validate_image_extension, validate_image_size
from .encryption import decrypt, encrypt, make_hash

# Create your models here.

class Province(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên tỉnh/ thành phố")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    code = models.CharField(max_length=10, blank=True)
    
    class Meta:
        verbose_name = "Tỉnh/Thành phố"
        verbose_name_plural = "Tỉnh/Thành phố"
        ordering = ["name"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.name
    
class Showroom(models.Model):
    brand = models.ForeignKey(
        "cars.Brand", on_delete=models.CASCADE, related_name="showrooms", verbose_name="Hãng xe"
    )
    province = models.ForeignKey(
        Province, on_delete=models.PROTECT, related_name="showrooms", verbose_name="Tỉnh/Thành phố"
        )
    name = models.CharField(max_length=250, verbose_name="Tên Showroom")
    address = models.CharField(max_length=300, verbose_name="Địa chỉ chi tiết")
    
    class Meta:
        verbose_name = "Showroom"
        verbose_name_plural = "Showroom"
        
    def __str__(self):
        return f"{self.name} ({self.province.name})"    
        
        
class User(AbstractUser):
    """
    Custom User model for CarCompare.

    Extends AbstractUser — keeps Django's full auth system (permissions,
    groups, admin, password hashing) while adding car-community fields.

    Social login (allauth) will call set_unusable_password() automatically.
    Users created via Google/Facebook have no password but can still log in.

    Sensitive fields use encrypt/decrypt pattern:
        - phone_encrypted: Fernet ciphertext, readable by admin
        - phone_hash: HMAC-SHA256, used for DB lookups without decrypting
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255, verbose_name="Email Address")
    class UserType(models.TextChoices):
        CUSTOMER = "customer", "Khách hàng"
        SALER = "saler", "Nhân viên tư vấn"
        WRITER = "writer", "Cộng tác viên"
        
    # =========Basic Profile============================
    bio = models.TextField(blank=True, help_text="Giới thiệu bản thân")
    avatar = models.ImageField(upload_to=UploadToPath(base_path="users", sub_path="avatars", slug_field="username"),
                               blank=True,
                               null=True,
                               validators=[validate_image_extension, validate_image_size]
                               )
    
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        help_text="Tỉnh/Thành phố đang sinh sống"
    )
    birth_year = models.PositiveSmallIntegerField(null=True, blank=True)
    user_type = models.CharField(
        max_length=20, choices=UserType.choices, default=UserType.CUSTOMER
    )
    
    # ── Encrypted fields — phone ─────────────────────────────────────────
    # phone_encrypted: readable by admin when needed
    # phone_hash: for DB lookups (check duplicate, verify) without decrypting
    phone_encrypted = models.TextField(blank=True)
    phone_hash = models.CharField(max_length=64, blank=True, db_index=True)
    
    
    # ── Encrypted fields — address ───────────────────────────────────────
    address_encrypted = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"
        
    def __str__(self) -> str:
        return self.username
    
    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"username": self.username})
    
    @property
    def display_name(self):
        """Full name if set, otherwise username."""
        return self.get_full_name() or self.username
    
    
    # ── Phone property ─────────────────────────────────────────────────
    @property
    def phone(self):
        """Decrypt and return phone number."""
        return decrypt(self.phone_encrypted)
    
    @phone.setter
    def phone(self, value):
        """
        Encrypt phone and store hash simultaneously.
        Calling user.phone = "0901234567" updates both fields at once —
        caller never touches phone_encrypted or phone_hash directly.
        """
        if value:
            self.phone_encrypted = encrypt(value)
            self.phone_hash = make_hash(value)
        else:
            self.phone_encrypted = ""
            self.phone_hash = ""
            
    
    # ── Address property ─────────────────────────────────────────────────
    @property
    def address(self):
        return decrypt(self.address_encrypted)
    
    @address.setter
    def address(self, value):
        if value:
            self.address_encrypted = encrypt(value)
        
        else:
            self.address_encrypted = ""
    
    
    # ── Helper ─────────────────────────────────────────────────
    @property
    def is_saler(self):
        return self.user_type == self.UserType.SALER
    
    @property
    def is_writer(self):
        return self.user_type == self.UserType.WRITER
    

# Saler Profile
class SalerProfile(models.Model):
    """
    Extended profile for saler users.
    Only exists when user.user_type == 'saler'
    
    Brand + City combination determines which saler appears on which
    variant detail page - a saler only show up when viewing cars belonging
    to their brand, filtered by city if user selects a region.
    
    is_verified must be True (set by admin) before saler appears publicly.
    """
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        related_name="saler_profile"
    )
    showroom = models.ForeignKey(
        Showroom,
        on_delete=models.SET_NULL,
        null=True,
        related_name="salers",
        verbose_name="Showroom"
    )
    employee_id = models.CharField(max_length=100, blank=True, verbose_name="Mã Nhân Viên")
    
    # ============CCCD encrypted=========
    cccd_encrypted = models.TextField(blank=True)
    cccd_hash = models.CharField(max_length=64, blank=True, db_index=True)
    
    # ==========Verification=============
    is_verified = models.BooleanField(
        default=False,
        help_text="Admin xác minh trước khi hiển thị công khai"
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Hồ sơ nhân viên tư vấn"
        verbose_name_plural = "Hồ sơ nhân viên tư vấn"
        
    def __str__(self) -> str:
        return f"{self.user.display_name} - {self.showroom}"
    
    # ── CCCD property ────────────────────────────────────────────────────
    @property
    def cccd(self):
        return decrypt(self.cccd_encrypted)
    
    @cccd.setter
    def cccd(self, value:str):
        if value:
            self.cccd_encrypted = encrypt(value)
            self.cccd_hash = make_hash(value)
        else:
            self.cccd_encypted = ""
            self.cccd_hash = ""
            
class SavedCar(models.Model):
    """
    A variant bookmarked by a user.
    unique_together ensures one user cannot save the same variant twice.
    """
    
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="saved_cars"
    )
    car = models.ForeignKey(
        "cars.CarVariant",
        on_delete=models.CASCADE,
        related_name="saved_by"
    )
    
    saved_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    
    class Meta:
        unique_together = ["user", "car"]
        ordering = ["-saved_at"]
        verbose_name = "Xe đã lưu"
        verbose_name_plural = "Xe đã lưu"
        
    def __str__(self):
        return f"{self.user.username} -> {self.car}"
    
    