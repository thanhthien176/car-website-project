from django.db import models
from ..car_models import CarVariant
from ..mixins import SpecificationDisplayMixin


class FuelConsumptionSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(
        CarVariant, on_delete=models.CASCADE, related_name='fuel_consumption'
    )

    emission_standards = models.CharField(
        max_length=100, blank=True, help_text="Tiêu chuẩn khí thải"
    )
    urban = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True,
        help_text="Mức tiêu thụ trong đô thị (L/100km)"
    )
    extra_urban = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True,
        help_text="Mức tiêu thụ ngoài đô thị (L/100km)"
    )
    combined = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True,
        help_text="Mức tiêu thụ kết hợp (L/100km)"
    )

    class Meta:
        verbose_name = "Nhiên Liệu"
        verbose_name_plural = "Nhiên Liệu"

    def __str__(self):
        return f"Fuel - {self.variant}"