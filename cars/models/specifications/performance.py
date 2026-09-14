from django.db import models
from ..car_models import CarVariant
from ..mixins import SpecificationDisplayMixin


class PerformanceSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(
        CarVariant, on_delete=models.CASCADE, related_name='performance'
    )

    # ===== Suspension System — MERGED =====
    suspension = models.CharField(
        max_length=300, blank=True,
        help_text="Hệ thống treo"
    )

    # ===== Braking System — COMBINED =====
    brake = models.CharField(
        max_length=300, blank=True,
        help_text="Hệ thống phanh"
    )

    # ===== Drive =====
    power_steering = models.CharField(
        max_length=100, blank=True, help_text="Trợ lực tay lái"
    )

    # ===== Tires & Rims =====
    rim = models.CharField(
        max_length=150, blank=True, help_text="Vành xe"
    )
    tire = models.CharField(
        max_length=150, blank=True, help_text="Lốp xe"
    )
    spare_tire = models.CharField(
        max_length=150, blank=True, help_text="Lốp dự phòng"
    )

    class Meta:
        verbose_name = "Vận Hành"
        verbose_name_plural = "Vận Hành"

    def __str__(self):
        return f"Performance - {self.variant}"