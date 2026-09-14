from django.db import models
from ..car_models import CarVariant
from ..mixins import SpecificationDisplayMixin


class SecureSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(
        CarVariant, on_delete=models.CASCADE, related_name='secure'
    )

    alarm_system = models.BooleanField(
        default=False, help_text="Hệ thống báo động"
    )
    eis = models.BooleanField(
        default=False, help_text="Mã hóa khóa động cơ (Immobilizer)"
    )

    class Meta:
        verbose_name = "An Ninh"
        verbose_name_plural = "An Ninh"

    def __str__(self):
        return f"Secure - {self.variant}"