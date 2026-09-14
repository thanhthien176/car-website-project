from django.db import models
from ..car_models import CarVariant
from ..mixins import SpecificationDisplayMixin


class EngineSpecification(SpecificationDisplayMixin, models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Tự động'),
        ('manual', 'Số sàn'),
        ('cvt', 'CVT'),
        ('dct', 'Ly hợp kép'),
        ('other', 'Khác'),
    ]

    variant = models.OneToOneField(
        CarVariant, on_delete=models.CASCADE, related_name='engine'
    )

    # ===== Internal Combustion Engine =====
    engine_type = models.CharField(
        max_length=150, blank=True, help_text="Loại động cơ"
    )
    number_of_cylinders = models.CharField(
        max_length=50, blank=True, help_text="Số xy lanh"
    )
    cylinder_arrangement = models.CharField(
        max_length=150, blank=True, help_text="Bố trí xy lanh"
    )
    displacement = models.CharField(
        max_length=100, blank=True, help_text="Dung tích xy lanh (cc)"
    )
    variable_valve_system = models.CharField(
        max_length=150, blank=True, help_text="Hệ thống van biến thiên"
    )
    compression_ratio = models.CharField(
        max_length=50, blank=True, help_text="Tỉ số nén"
    )
    max_power = models.CharField(
        max_length=150, blank=True, help_text="Công suất tối đa"
    )
    max_torque = models.CharField(
        max_length=150, blank=True, help_text="Mô men xoắn cực đại"
    )

    # ===== Electric / Hybrid Engine =====
    electric_motor_mp = models.CharField(
        max_length=150, blank=True, help_text="Công suất tối đa động cơ điện"
    )
    electric_motor_mt = models.CharField(
        max_length=150, blank=True, help_text="Mô men xoắn tối đa động cơ điện"
    )
    hybrid_batteries = models.CharField(
        max_length=150, blank=True, help_text="Ắc quy hybrid"
    )

    # ===== Transmission =====
    drive_train = models.CharField(
        max_length=150, blank=True, help_text="Hệ thống dẫn động"
    )
    transmission = models.CharField(
        max_length=150, blank=True, choices=TRANSMISSION_CHOICES,
        help_text="Hộp số"
    )
    drive_mode = models.CharField(
        max_length=200, blank=True, help_text="Các chế độ lái"
    )

    class Meta:
        verbose_name = "Động Cơ"
        verbose_name_plural = "Động Cơ"

    def __str__(self):
        return f"Engine - {self.variant}"