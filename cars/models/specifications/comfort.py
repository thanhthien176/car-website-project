from django.db import models
from ..car_models import CarVariant
from ..mixins import SpecificationDisplayMixin


class ComfortSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(
        CarVariant, on_delete=models.CASCADE, related_name='comfort'
    )

    # ===== Air Conditioner =====
    air_conditioner = models.CharField(
        max_length=150, blank=True, help_text="Hệ thống điều hòa"
    )
    rear_air_duct = models.BooleanField(
        default=False, help_text="Cửa gió hàng ghế sau"
    )
    cooler_box = models.BooleanField(
        default=False, help_text="Hộp làm mát"
    )

    # ===== Sunshade curtain =====
    rear_window_sunshade = models.CharField(
        max_length=150, blank=True, help_text="Rèm che nắng kính sau"
    )
    rear_door_sunshade = models.CharField(
        max_length=150, blank=True, help_text="Rèm che nắng cửa sau"
    )

    # ===== Entertainment =====
    display = models.CharField(
        max_length=200, blank=True, help_text="Màn hình giải trí"
    )
    display_info_windsheld = models.BooleanField(
        default=False, help_text="Hiển thị thông tin trên kính lái (HUD)"
    )
    speaker = models.CharField(
        max_length=100, blank=True, help_text="Âm thanh"
    )
    smart_connect = models.CharField(
        max_length=200, blank=True, help_text="Kết nối thông minh"
    )
    bluetooth = models.BooleanField(
        default=False, help_text="Kết nối Bluetooth"
    )
    
    usb_connect = models.CharField(
        max_length=200, blank=True, help_text="Kết nối usb"
    )
    
    wireless_charging = models.BooleanField(
        default=False, help_text="Sạc không dây"
    )
    voice_control = models.BooleanField(
        default=False, help_text="Điều khiển bằng giọng nói"
    )
    hands_free_calling = models.BooleanField(
        default=False, help_text="Đàm thoại rảnh tay"
    )
    smart_mobile_connect = models.BooleanField(
        default=False, help_text="Kết nối điện thoại thông minh"
    )
    control_rear_seat = models.BooleanField(
        default=False, help_text="Điều khiển từ hàng ghế sau"
    )

    # ===== Other amenities =====
    smart_key = models.BooleanField(
        default=False, help_text="Chìa khóa thông minh & khởi động nút bấm"
    )
    power_door = models.BooleanField(
        default=False, help_text="Khóa cửa điện"
    )
    remote_door = models.BooleanField(
        default=False, help_text="Khóa cửa từ xa"
    )
    power_window = models.CharField(
        max_length=150, blank=True, help_text="Cửa sổ điều chỉnh điện"
    )
    car_trunk = models.CharField(
        max_length=200, blank=True, help_text="Cốp xe"
    )
    cruise_control = models.CharField(
        max_length=200, blank=True,
        help_text="Điều khiển hành trình"
    )
    electric_parking_brake = models.BooleanField(
        default=False, help_text="Phanh tay điện tử (EPB)"
    )
    brake_hold = models.BooleanField(
        default=False, help_text="Giữ phanh tự động (Auto Hold)"
    )

    class Meta:
        verbose_name = "Tiện Lợi"
        verbose_name_plural = "Tiện Lợi"

    def __str__(self):
        return f"Comfort - {self.variant}"