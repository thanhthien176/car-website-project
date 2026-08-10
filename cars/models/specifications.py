from django.db import models

from .car_models import CarVariant
from .mixins import SpecificationDisplayMixin

class DimensionSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='dimension')
    
    overall_dimensions = models.CharField(max_length=100, blank=True, help_text="Kích thước tổng thể (DxRxC)")
    length = models.PositiveIntegerField(null=True, blank=True, help_text="Chiều dài(mm)")
    width = models.PositiveIntegerField(null=True, blank=True, help_text="Chiều rộng(mm)")
    height = models.PositiveIntegerField(null=True, blank=True, help_text="chiều cao(mm)")
    
    turning_radius = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Bán kính vòng quay tối thiểu (m)")
    
    wheelbase = models.PositiveIntegerField(null=True, blank=True, help_text="Chiều dài cơ sở(mm)")
    ground_clearance = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Khoảng sáng gầm xe(mm)")
    
    unloaded_weight = models.PositiveIntegerField(null=True, blank=True, help_text="Trọng lượng không tải (kg)")
    full_loaded_weight = models.PositiveIntegerField(null=True, blank=True, help_text="Trọng lượng toàn tải (kg)")   
    seating_capacity = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Số chỗ ngồi")
    fuel_tank_capacity = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Dung tích bình nhiên liệu(lít)")
    
    class Meta:
        verbose_name = "Tổng Thể"
    
class EngineSpecification(SpecificationDisplayMixin, models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Tự động'),
        ('manual', 'Số sàn'),
        ('cvt', 'CVT'),
    ]
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='engine')
    
     # Engine - performance
    engine_type = models.CharField(max_length=100, blank=True, help_text="Loại động cơ")
    
    number_of_cylinders = models.CharField(max_length=100, blank=True, help_text="Số xy lanh")
    cylinder_arrangement = models.CharField(max_length=50, blank=True, help_text="Bố trí xy lanh")
    displacement = models.CharField(max_length=50, blank=True, help_text="Dung tích xi lanh(cc)")
    variable_valve_system = models.CharField(max_length=50, blank=True, help_text="Hệ thống van biến thiên")
    compression_ratio = models.CharField(max_length=50, blank=True, help_text="Tỉ số nén")
    
    max_power = models.CharField(max_length=100, blank=True, help_text="Công suất tối đa(Hp)")
    max_torque = models.CharField(max_length=100, blank=True, help_text="Momen xoắn tối đa(Nm)")
    
    # electric motor
    electric_motor_mp = models.CharField(max_length=50, blank=True, help_text="Công suất tối đa KW (động cơ điện)")
    electric_motor_mt = models.CharField(max_length=50, blank=True, help_text="Momen xoắn tối đa Nm")
    hybrid_batteries = models.CharField(max_length=50, blank=True, help_text="Ắc quy hybrid")
    
    drive_mode = models.CharField(max_length=100, blank=True, help_text="Các chế độ lái")
    drive_train = models.CharField(max_length=50, blank=True, help_text="Hệ thống truyền động")
    transmission = models.CharField(max_length=40, choices=TRANSMISSION_CHOICES, help_text="Hộp số")
    
    
    class Meta:
            verbose_name = "Động Cơ"

class PerformanceSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='performance')
    
    # suspension
    suspension = models.CharField(max_length=100, blank=True, help_text="Hệ thống treo")
    suspension_font = models.CharField(max_length=50, blank=True, help_text="Hệ thống treo trước")
    suspension_rear = models.CharField(max_length=50, blank=True, help_text="Hệ thống treo sau")

    power_steering = models.CharField(max_length=100, blank=True, help_text="Trợ lực tay lái")
    
    
    # Tire & wheel
    rim_type = models.CharField(max_length=50, blank=True, help_text="Loại vành")
    tire_size = models.CharField(max_length=50, blank=True, help_text="Kích thước lốp xe")
    spare_tire = models.CharField(max_length=50, blank=True, help_text="Lốp dự phòng")
    
    brake = models.CharField(max_length=50, blank=True, help_text="Hệ thống phanh trước/sau(front/rear)")
    brake_front = models.CharField(max_length=50, blank=True, help_text="Hệ thống phanh trước")
    brake_rear = models.CharField(max_length=50, blank=True, help_text="Hệ thống phanh sau")
    
    class Meta:
            verbose_name = "Vận Hành"    
    
class FuelConsumptionSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='fuel_consumption')
    
    # fuel comsumption
    emission_standards = models.CharField(max_length=50, blank=True, help_text="Tiêu chuẩn khí thải")
    urban = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Mức tiêu thụ trong đô thị(lit/100km)")
    extra_urban = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Mức tiêu thụ ngoài đô thị(lít/100km)")
    combined = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Mức tiêu thụ kết hợp(lít/100km)")
    
    class Meta:
            verbose_name = "Nhiên Liệu"
class ExteriorSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='exterior')
    
    # exterior
    headlamp = models.CharField(max_length=50, blank=True, help_text="Đèn chiếu sáng trước")
    low_beam_headlight = models.CharField(max_length=50, blank=True, help_text="Đèn chiếu gần trước")
    high_beam_headlight = models.CharField(max_length=50, blank=True, help_text="Đèn chiếu xa")
    light_on_reminder = models.BooleanField(default=False, help_text="Hệ thống nhắc nhở đèn sáng")
    cornering_light = models.BooleanField(default=False, help_text="Đèn chiếu góc")
    hls = models.CharField(max_length=50, blank=True, help_text="Hệ thống cân bằng góc chiếu")
    
    daytime_running_light = models.BooleanField(default=False, help_text="Đèn chiếu sáng ban ngày")
    auto_light_control = models.BooleanField(default=False, help_text="Tự động bật tắt đèn")
    pabs = models.CharField(max_length=50, blank=True, help_text="Hệ thống cân bằng góc chiếu ")    # (Projection angle balancing system) 
    nlm = models.BooleanField(default=False, help_text="Chế độ đèn chờ dẫn đường")                  # (Navigation light mode)
    
    rearlamp = models.CharField(max_length=50, blank=True, help_text="Đèn hậu")
    foglamp = models.CharField(max_length=50, blank=True, help_text="Đèn sương mù")
    
    position_light = models.CharField(max_length=50, blank=True, help_text="Đèn vị trí")
    brake_light = models.CharField(max_length=50, blank=True, help_text="Đèn phanh")
    reverse_light = models.CharField(max_length=50, blank=True, help_text="Đèn lùi")
    turn_signal_lamp = models.CharField(max_length=50, blank=True, help_text="Tích hợp đèn báo rẽ")
    
    third_brake_lamp = models.CharField(max_length=50, blank=True, help_text="Đèn phanh trên cao, đèn phanh thứ 3")
    
    foglamp_front = models.CharField(max_length=50, blank=True, help_text="Đèn sương mù trước")
    foglamp_rear = models.CharField(max_length=50, blank=True, help_text="Đèn sương mù sau")
    
    # Outer mirrors
    power_fold_mirror = models.BooleanField(default=False, help_text="Gập điện")
    power_adjust_mirror = models.BooleanField(default=False, help_text="Điều chỉnh bằng điện")
    itsl = models.BooleanField(default=False, help_text="Tích hợp đèn báo rẽ")
    iwl = models.BooleanField(default=False, help_text="Tích hợp đèn chào mừng")
    self_adjust_reverse = models.BooleanField(default=False, help_text="Tự điều chỉnh khi lùi")
    mirror_memory = models.BooleanField(default=False, help_text="Nhớ vị trí gương")
    mirror_color = models.CharField(max_length=50, blank=True, help_text="Màu gương")
    
    # wiper
    wiper_front = models.CharField(max_length=50, blank=True, help_text="Gạt mưa trước")
    wiper_rear = models.CharField(max_length=50, blank=True, help_text="Gạt mưa sau")
    rear_glass_defrogger = models.BooleanField(default=False, help_text="Chức năng sấy kính sau")
    
    antenna = models.CharField(max_length=50, blank=True, help_text="Ăng ten")
    outside_handle = models.CharField(max_length=50, blank=True, help_text="Tay nắm cửa ngoài xe")
    
    bumper_bar = models.CharField(blank=True, max_length=100, help_text="Thanh cản trước và sau")
    bumper_bar_front = models.BooleanField(default=False, help_text="Thanh cản trước")
    bumper_bar_rear = models.BooleanField(default=False, help_text="Thanh cản sau")
    
    mudguard = models.CharField(max_length=40, blank=True, help_text="Chắn bùn")
    support_bar = models.BooleanField(default=False, help_text="Thanh đỡ nóc xe")
    
    class Meta:
            verbose_name = "Ngoại Thất"
    
class InteriorSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='interior')
    
    # Interior
    steering_type = models.CharField(max_length=50, blank=True, help_text="Loại tay lái")
    steering_material = models.CharField(max_length=50, blank=True, help_text="Chất liệu tay lái")
    steering_adjust = models.CharField(max_length=50, blank=True, help_text="Điều chỉnh tay lái")
    paddle_shifter = models.BooleanField(default=False, help_text="Lẫy chuyển số")
    icb = models.CharField(max_length=200, blank=True, help_text="Nút bấm điều khiển tích hơp (Integrated control buttons)")     
    steering_memory = models.BooleanField(default=False, help_text="Nhớ vị trí tay lái")
    power_steering = models.CharField(max_length=100, blank=True, help_text="Trợ lực tay lái")
    
    inner_mirror = models.CharField(max_length=50, blank=True, help_text="Gương chiếu hậu trong")
    inside_handle_door = models.CharField(max_length=50, blank=True, help_text="Tay nắm cửa trong xe")
    
    combination_metter = models.CharField(max_length=50, blank=True, help_text="Cụm đồng hồ")
    metter_type = models.CharField(max_length=50, blank=True, help_text="Loại đồng hồ")
    eco_signal = models.BooleanField(default=False, help_text="Đèn báo chế độ Eco")
    hybrid_signal = models.BooleanField(default=False, help_text="Đèn báo chế độ Hybrid")
    fcif = models.BooleanField(default=False, help_text="Chức năng báo tiêu thụ nhiên liệu")
    gear_position = models.BooleanField(default=False, help_text="Chức năng báo vị trí cần số")
    multi_info_display = models.CharField(max_length=100, blank=True, help_text="Màn hình hiển thị đa thông tin")
    
    
    sunroof = models.CharField(max_length=50, blank=True, help_text="Cửa sổ trời")
    
    class Meta:
            verbose_name = "Nội Thất"
    
class SeatSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='seat')
    
    # Seat
    seat_material = models.CharField(max_length=50, blank=True, help_text="Chất liệu bọc ghế")
    
    front_seat_type = models.CharField(max_length=50, blank=True, help_text="Loại ghế trước")
    driver_seat = models.CharField(max_length=50, blank=True, help_text="Điều chỉnh ghế lái")
    front_passeger_seat = models.CharField(max_length=50, blank=True, help_text="Điều chỉnh ghế hành khách")
    seat_memory = models.CharField(max_length=50, blank=True, help_text="Bộ nhớ vị trí ghế")
    
    rear_seat = models.CharField(max_length=50, blank=True, help_text="Ghế sau")
    second_seat = models.CharField(max_length=100, blank=True, help_text="Hàng ghế thứ hai")
    third_seat = models.CharField(max_length=100, blank=True, help_text="Hàng ghế thứ ba")
    rear_seat_armset = models.CharField(max_length=50, blank=True, help_text="Tựa tay hàng ghế sau")
    
    
    class Meta:
            verbose_name = "Ghế Ngồi"
class ComfortSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='comfort')
    
    # Utilities & Comfort
    air_conditioner = models.CharField(max_length=100, blank=True, help_text="Hệ thống điều hòa")
    rear_air_duct = models.BooleanField(default=False, help_text="Cửa gió sau")
    cooler_box = models.BooleanField(default=False, help_text="Hộp làm mát")
    
    rear_window_sunshade = models.CharField(max_length=100, blank=True, help_text="Rèm che nắng phía sau")
    rear_door_sunshade = models.CharField(max_length=100, blank=True, help_text="Rèm che nắng cửa sau")
    
    
    display = models.CharField(max_length=50, blank=True, help_text="Màn hình giải trí")
    display_info_windsheld = models.BooleanField(default=False, help_text="Hiển thị thông tin trên kính lái")
    
    number_of_speaker = models.CharField(max_length=50, blank=True, help_text="Số loa")
    smart_connect = models.CharField(max_length=50, blank=True, help_text="Kết nối không dây")
    usb_connect_front = models.BooleanField(default=False, help_text="Cổng kết nối usb")
    usb_connect_rear = models.BooleanField(default=False, help_text="Cổng kết nối phía sau")
    wireless_charging = models.BooleanField(default=False, help_text="Sạc không dây")
    bluetooth = models.BooleanField(default=False, help_text="Kết nối bluetooth")
    voice_control = models.BooleanField(default=False, help_text="Hệ thống điều khiển bằng giọng nói")
    
    control_rear_seat = models.BooleanField(default=False, help_text="Chức năng điều khiển từ hàng ghế sau") 
    hands_free_calling = models.BooleanField(default=False, help_text="Hệ thống đàm thoại rảnh tay")
    smart_mobile_connect = models.BooleanField(default=False, help_text="Kết nối điện thoại thông minh không dây")
    
    smart_key = models.BooleanField(default=False, help_text="Chìa khóa thông minh")
    power_door = models.BooleanField(default=False, help_text="Khóa cửa điện")
    remote_door = models.BooleanField(default=False, help_text="Chức năng khóa cửa từ xa")
    
    power_window = models.CharField(max_length=50, blank=True, help_text="Cửa sổ điều chỉnh điện")
    power_back_door = models.BooleanField(default=False, help_text="Cốp điện")
    cruise_control = models.BooleanField(default=False, help_text="Hệ thống điều khiển hành trình (ga tự động)")
    electric_parking_brake = models.BooleanField(default=False, help_text="Phanh tay điện tủ")
    brake_hold = models.BooleanField(default=False, help_text="Giữ phanh tự động")
    
    class Meta:
            verbose_name = "Tiện Lợi"

class SecureSpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='secure')
    
    alarm_system = models.BooleanField(default=False, help_text="Hệ thống báo động (An ninh)")
    eis = models.BooleanField(default=False, help_text="Hệ thống mã hóa khóa động cơ")
    
    class Meta:
            verbose_name = "An Ninh"
    
class SafetySpecification(SpecificationDisplayMixin, models.Model):
    variant = models.OneToOneField(CarVariant, on_delete=models.CASCADE, related_name='safety')
    
    # active safety
    pcs = models.BooleanField(default=False, help_text="Cảnh báo tiền va chạm(pre-collision warning)")
    lda = models.BooleanField(default=False, help_text="Cảnh báo lệch làn đường(Lane departure alert)")
    lta = models.BooleanField(default=False, help_text="Hỗ trợ giữ làn đường(lane tracing assist)")
    
    drcc = models.BooleanField(default=False, help_text="Hệ thống điều khiển hành trình chủ động(Dynamic radar cruise control)")
    ahb = models.BooleanField(default=False, help_text="Đèn chiếu xa tự động(Automatic high beam)")
    
    reverse_camera = models.BooleanField(default=False, help_text="Camera lùi")
    camera_360 = models.BooleanField(default=False, help_text="Camera 360")
    parking_camera = models.CharField(max_length=50, blank=True, help_text="camera hỗ trợ đỗ xe")
    parking_brake = models.BooleanField(default=False, help_text="Phanh hỗ trợ đổ xe")
    
    bsm = models.BooleanField(default=False, help_text="Hế thống cảnh báo điểm mù(Blind spot monitor)")
    rcta = models.BooleanField(default=False, help_text="Hệ thống hỗ trợ phương tiện cắt ngang phía sau(Rear cross traffic alert)")
    
    abs = models.BooleanField(default=False, help_text="Hệ thống chống bó cứng phanh(Anti-lock braking system)")
    ba = models.BooleanField(default=False, help_text="Hệ thống hỗ trợ lực phanh khẩn cấp(Brake assist)")
    ebd = models.BooleanField(default=False, help_text="Hệ thống phân phối lực phanh điện từ(Electronic brake-force distribution)")
    vsc = models.BooleanField(default=False, help_text="Hệ thống cân bằng điện tử(vehicle stability control")
    trc = models.BooleanField(default=False, help_text="Hệ thống kiểm soát lực kéo(Traction control")
    hac = models.BooleanField(default=False, help_text="Hệ thống hỗ trợ khởi hành ngang dốc(Hill-start assist control")
    ebs = models.BooleanField(default=False, help_text="Hệ thống đèn báo phanh khẩn cấp(Emergency brake signal)")
    tpws = models.BooleanField(default=False, help_text="Hệ thống cảnh báo áp suất lốp(Tyre pressure warning system)")
    tpms = models.BooleanField(default=False, help_text="Hệ thống theo dõi áp suất lốp")
    
    # Parking assist sensor
    sensor = models.CharField(max_length=100, blank=True, help_text="Cảm biến hỗ trợ đổ xe")
    sensor_front = models.BooleanField(default=False, help_text="Cảm biến hỗ trợ đổ xe trước")
    sensor_front_corner = models.BooleanField(default=False, help_text="Cảm biến hỗ trợ đổ xe góc trước")
    sensor_rear_corner = models.BooleanField(default=False, help_text="Cảm biến hỗ trợ đổ xe góc sau")
    sensor_rear = models.BooleanField(default=False, help_text="Cảm biến hỗ trợ đổ xe phía sau")
    
    airbag = models.CharField(max_length=50, blank=True, help_text="Túi khí")
    font_airbag = models.CharField(max_length=50, blank=True, help_text="Túi khí phía trước")
    front_side_airbag = models.CharField(max_length=50, blank=True, help_text="Túi khí bên hông phía trước")
    curtain_airbag = models.CharField(max_length=50, blank=True, help_text="Túi khí rèm")
    driver_knee_airbag = models.CharField(max_length=50, blank=True, help_text="Túi khí đầu gối người lái")
    
    seat_belt = models.CharField(max_length=50, blank=True, help_text="Dây đai an toàn")
    child_safety_lock = models.CharField(max_length=50, blank=True, help_text="Khóa an toàn trẻ em")
    secure_door = models.BooleanField(default=False, help_text="Khóa cửa an toàn")
    exit_safety = models.BooleanField(default=False, help_text="Hệ thống hỗ trợ ra khỏi xe an toàn")
    
    safety_rating = models.PositiveSmallIntegerField(null=True, blank=True, help_text="Sao NCAP")
    
    class Meta:
            verbose_name = "An Toàn"
    # @property
    # def boolean_safety_items(self):
    #     items = []
    #     for field in self._meta.get_fields():
    #         if isinstance(field, models.BooleanField):
    #             value = getattr(self, field.name)
                
    #             items.append({
    #                 'short_name': field.name.upper(),
    #                 'help_text': field.help_text or '',
    #                 'value': value,
    #             })
        
    #     return items