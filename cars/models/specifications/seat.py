from django.db import models
from ..car_models import CarVariant
from ..mixins import SpecificationDisplayMixin


class SeatSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(
        CarVariant, on_delete=models.CASCADE, related_name='seat'
    )

    seat_material = models.CharField(
        max_length=150, blank=True, help_text="Chất liệu bọc ghế"
    )
    seat_type = models.CharField(
        max_length=150, blank=True, help_text="Loại ghế"
    )

    # ===== Front seat =====
    front_seat_type = models.CharField(
        max_length=150, blank=True, help_text="Loại ghế trước"
    )
    driver_seat = models.CharField(
        max_length=200, blank=True, help_text="Điều chỉnh ghế lái"
    )
    front_passenger_seat = models.CharField(
        max_length=200, blank=True,
        help_text="Điều chỉnh ghế hành khách phía trước"
    )
    seat_memory = models.CharField(
        max_length=150, blank=True, help_text="Bộ nhớ vị trí ghế"
    )

    # ===== Rear seat =====
    rear_seat = models.CharField(
        max_length=200, blank=True, help_text="Ghế sau"
    )
    second_seat = models.CharField(
        max_length=200, blank=True, help_text="Hàng ghế thứ hai"
    )
    third_seat = models.CharField(
        max_length=200, blank=True, help_text="Hàng ghế thứ ba"
    )
    rear_seat_armrest = models.CharField(
        max_length=150, blank=True, help_text="Tựa tay hàng ghế sau"
    )

    class Meta:
        verbose_name = "Ghế Ngồi"
        verbose_name_plural = "Ghế Ngồi"

    def __str__(self):
        return f"Seat - {self.variant}"