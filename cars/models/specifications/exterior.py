from django.db import models
from ..car_models import CarVariant
from ..mixins import SpecificationDisplayMixin


class ExteriorSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(
        CarVariant, on_delete=models.CASCADE, related_name='exterior'
    )

    # ===== Front light =====
    headlamp = models.CharField(
        max_length=200, blank=True, help_text="Cụm đèn chiếu sáng trước"
    )
    low_beam_headlight = models.CharField(
        max_length=150, blank=True, help_text="Đèn chiếu gần"
    )
    high_beam_headlight = models.CharField(
        max_length=150, blank=True, help_text="Đèn chiếu xa"
    )
    daytime_running_light = models.CharField(
        max_length=150, blank=True, help_text="Đèn chiếu sáng ban ngày (DRL)"
    )
    cornering_light = models.BooleanField(
        default=False, help_text="Đèn chiếu góc"
    )
    light_on_reminder = models.BooleanField(
        default=False, help_text="Nhắc nhở đèn sáng"
    )
    auto_light_control = models.BooleanField(
        default=False, help_text="Tự động bật/tắt đèn"
    )
    # MERGE: hls + pabs → 1 field (same meaning as 'projection angle balance')
    projection_angle_balance = models.CharField(
        max_length=150, blank=True,
        help_text="Hệ thống cân bằng góc chiếu (PABS)"
    )
    navigation_light_mode = models.BooleanField(
        default=False, help_text="Chế độ đèn chờ dẫn đường"
    )

    # ===== Rear light =====
    rearlamp = models.CharField(
        max_length=200, blank=True, help_text="Cụm đèn hậu"
    )
    brake_light = models.CharField(
        max_length=150, blank=True, help_text="Đèn phanh"
    )
    third_brake_lamp = models.CharField(
        max_length=150, blank=True, help_text="Đèn phanh trên cao"
    )
    reverse_light = models.CharField(
        max_length=150, blank=True, help_text="Đèn lùi"
    )
    position_light = models.CharField(
        max_length=150, blank=True, help_text="Đèn vị trí"
    )
    turn_signal_lamp = models.CharField(
        max_length=150, blank=True, help_text="Đèn báo rẽ"
    )
    foglamp_front = models.CharField(
        max_length=150, blank=True, help_text="Đèn sương mù trước"
    )
    foglamp_rear = models.CharField(
        max_length=150, blank=True, help_text="Đèn sương mù sau"
    )

    # ===== Exterior Rearview Mirror =====
    mirror = models.CharField(
        max_length=200, blank=True, help_text="Gương chiếu hậu ngoài"
    )
    mirror_color = models.CharField(
        max_length=150, blank=True, help_text="Màu gương"
    )
    power_adjust_mirror = models.BooleanField(
        default=False, help_text="Chỉnh điện"
    )
    power_fold_mirror = models.BooleanField(
        default=False, help_text="Gập điện"
    )
    mirror_heating = models.BooleanField(
        default=False, help_text="Sấy gương"
    )
    mirror_memory = models.BooleanField(
        default=False, help_text="Nhớ vị trí gương"
    )
    self_adjust_reverse = models.BooleanField(
        default=False, help_text="Tự điều chỉnh khi lùi"
    )
    itsl = models.BooleanField(
        default=False, help_text="Tích hợp đèn báo rẽ trên gương"
    )
    iwl = models.BooleanField(
        default=False, help_text="Tích hợp đèn chào mừng"
    )

    # ===== Wipers & Glass =====
    wiper_front = models.CharField(
        max_length=150, blank=True, help_text="Gạt mưa trước"
    )
    wiper_rear = models.CharField(
        max_length=150, blank=True, help_text="Gạt mưa sau"
    )
    rear_glass_defogger = models.BooleanField(
        default=False, help_text="Sấy kính sau"
    )
    sunroof = models.CharField(
        max_length=100, blank=True, help_text="Cửa sổ trời"
    )

    # ===== Exterior Details =====
    antenna = models.CharField(
        max_length=150, blank=True, help_text="Ăng ten"
    )
    outside_handle = models.CharField(
        max_length=150, blank=True, help_text="Tay nắm cửa ngoài"
    )
    # MERGE: bumper_bar + bumper_bar_front + bumper_bar_rear
    bumper_bar = models.CharField(
        max_length=200, blank=True,
        help_text="Thanh cản"
    )
    mudguard = models.CharField(
        max_length=150, blank=True, help_text="Chắn bùn"
    )
    support_bar = models.BooleanField(
        default=False, help_text="Thanh đỡ nóc xe (giá nóc)"
    )

    class Meta:
        verbose_name = "Ngoại Thất"
        verbose_name_plural = "Ngoại Thất"

    def __str__(self):
        return f"Exterior - {self.variant}"