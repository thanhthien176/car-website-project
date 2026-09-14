from django.db import models
from ..car_models import CarVariant
from ..mixins import SpecificationDisplayMixin


class InteriorSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(
        CarVariant, on_delete=models.CASCADE, related_name='interior'
    )

    # ===== Steering Wheel =====
    steering_type = models.CharField(
        max_length=150, blank=True, help_text="Loại tay lái"
    )
    steering_material = models.CharField(
        max_length=100, blank=True, help_text="Chất liệu tay lái"
    )
    steering_adjust = models.CharField(
        max_length=100, blank=True, help_text="Điều chỉnh tay lái"
    )
    paddle_shifter = models.BooleanField(
        default=False, help_text="Lẫy chuyển số sau vô lăng"
    )
    steering_memory = models.BooleanField(
        default=False, help_text="Nhớ vị trí tay lái"
    )
    icb = models.CharField(
        max_length=200, blank=True,
        help_text="Nút bấm điều khiển tích hợp trên vô lăng"
    )

    # ===== Mirror inside & handle =====
    inner_mirror = models.CharField(
        max_length=100, blank=True, help_text="Gương chiếu hậu trong"
    )
    inside_handle_door = models.CharField(
        max_length=100, blank=True, help_text="Tay nắm cửa trong"
    )

    # ===== Dashboard Cluster =====
    combination_meter = models.CharField(
        max_length=100, blank=True, help_text="Cụm đồng hồ"
    )
    meter_type = models.CharField(
        max_length=100, blank=True, help_text="Loại đồng hồ"
    )
    multi_info_display = models.CharField(
        max_length=150, blank=True, help_text="Màn hình hiển thị đa thông tin"
    )
    eco_signal = models.BooleanField(
        default=False, help_text="Đèn báo chế độ Eco"
    )
    hybrid_signal = models.BooleanField(
        default=False, help_text="Đèn báo chế độ Hybrid"
    )
    fcif = models.BooleanField(
        default=False, help_text="Chức năng báo tiêu thụ nhiên liệu"
    )
    gear_position = models.BooleanField(
        default=False, help_text="Chức năng báo vị trí cần số"
    )

    class Meta:
        verbose_name = "Nội Thất"
        verbose_name_plural = "Nội Thất"

    def __str__(self):
        return f"Interior - {self.variant}"