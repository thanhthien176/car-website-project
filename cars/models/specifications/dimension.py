from django.db import models
from ..car_models import CarVariant
from ..mixins import SpecificationDisplayMixin


class DimensionSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(
        CarVariant, on_delete=models.CASCADE, related_name='dimension'
    )

    overall_dimensions = models.CharField(
        max_length=100, blank=True,
        help_text="Kích thước tổng thể (DxRxC) (mm)"
    )
    length = models.CharField(
        max_length=50, blank=True, help_text="Chiều dài (mm)"
    )
    width = models.CharField(
        max_length=50, blank=True, help_text="Chiều rộng (mm)"
    )
    height = models.CharField(
        max_length=50, blank=True, help_text="Chiều cao (mm)"
    )

    wheelbase = models.CharField(
        max_length=50, blank=True, help_text="Chiều dài cơ sở (mm)"
    )
    track_width = models.CharField(
        max_length=50, blank=True, help_text="Vết bánh xe trước/sau (mm)"
    )
    ground_clearance = models.CharField(
        max_length=150, blank=True, help_text="Khoảng sáng gầm xe (mm)"
    )
    turning_radius = models.CharField(
        max_length=50, blank=True, help_text="Bán kính quay vòng tối thiểu (m)"
    )

    unloaded_weight = models.CharField(
        max_length=150, blank=True, help_text="Trọng lượng không tải (kg)"
    )
    full_loaded_weight = models.CharField(
        max_length=150, blank=True, help_text="Trọng lượng toàn tải (kg)"
    )
    seating_capacity = models.CharField(
        max_length=150, blank=True, help_text="Số chỗ ngồi"
    )
    fuel_tank_capacity = models.CharField(
        max_length=150, blank=True, help_text="Dung tích bình nhiên liệu (Lít)"
    )

    class Meta:
        verbose_name = "Tổng Thể"
        verbose_name_plural = "Tổng Thể"

    def __str__(self):
        return f"Dimension - {self.variant}"