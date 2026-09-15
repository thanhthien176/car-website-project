from django.db import models
from ..car_models import CarVariant
from ..mixins import SpecificationDisplayMixin


class SafetySpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(
        CarVariant, on_delete=models.CASCADE, related_name='safety'
    )

    # ===== MERGED: Lane support (LDA + LKA + LTA) =====
    # (VD: Cảnh báo lệch làn + Hỗ trợ giữ làn)
    lane_keeping_assist = models.CharField(
        max_length=300, blank=True,
        help_text="Hỗ trợ làn đường"
    )

    # ===== COMBINE: Collision Prevention (PCS + BSM + RCTA) =====
    # (VD: Tiền va chạm + Điểm mù + Cắt ngang phía sau)
    collision_avoidance = models.CharField(
        max_length=300, blank=True,
        help_text="Phòng tránh va chạm"
    )

    # ===== Automatic high beam lights =====
    auto_high_beam = models.CharField(
        max_length=200, blank=True, help_text="Đèn chiếu xa tự động (AHB)"
    )

    # ===== Braking & stability system =====
    abs = models.BooleanField(
        default=False, help_text="Chống bó cứng phanh (ABS)"
    )
    ba = models.BooleanField(
        default=False, help_text="Hỗ trợ lực phanh khẩn cấp (BA)"
    )
    ebd = models.BooleanField(
        default=False, help_text="Phân phối lực phanh điện tử (EBD)"
    )
    vsc = models.BooleanField(
        default=False, help_text="Cân bằng điện tử (VSC/ESC)"
    )
    trc = models.BooleanField(
        default=False, help_text="Kiểm soát lực kéo (TRC/TCS)"
    )
    hac = models.BooleanField(
        default=False, help_text="Hỗ trợ khởi hành ngang dốc (HAC)"
    )
    ebs = models.BooleanField(
        default=False, help_text="Đèn báo phanh khẩn cấp (EBS)"
    )
    
    # ===== Tire Pressure =====
    tpms = models.BooleanField(
        default=False, help_text="Cảnh báo áp suất lốp (TPMS)"
    )

    # ===== Camera & parking sensors =====
    reverse_camera = models.BooleanField(
        default=False, help_text="Camera lùi"
    )
    camera_360 = models.BooleanField(
        default=False, help_text="Camera 360 độ"
    )
    parking_brake = models.BooleanField(
        default=False, help_text="Phanh hỗ trợ đỗ xe (PKSB)"
    )
    # MERGE: sensor + sensor_front + sensor_rear + sensor_front_corner + sensor_rear_corner
    # (VD: Trước + Sau + Góc trước + Góc sau)
    parking_sensor = models.CharField(
        max_length=300, blank=True,
        help_text="Cảm biến hỗ trợ đỗ xe"
    )

    # ===== Airbag =====
    #  (VD: 6 túi khí: Trước, bên hông, rèm, đầu gối)
    airbag = models.CharField(
        max_length=300, blank=True,
        help_text="Túi khí"
    )

    # ===== Passive Safety =====
    seat_belt = models.CharField(
        max_length=200, blank=True, help_text="Dây đai an toàn"
    )
    child_safety_lock = models.CharField(
        max_length=150, blank=True, help_text="Khóa an toàn trẻ em (ISOFIX)"
    )
    secure_door = models.BooleanField(
        default=False, help_text="Khóa cửa an toàn"
    )
    exit_safety = models.BooleanField(
        default=False, help_text="Hỗ trợ ra khỏi xe an toàn (SEA/SEW)"
    )

    # ===== Review =====
    safety_rating = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="Số sao NCAP"
    )

    class Meta:
        verbose_name = "An Toàn"
        verbose_name_plural = "An Toàn"

    def __str__(self):
        return f"Safety - {self.variant}"