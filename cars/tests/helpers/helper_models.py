from decimal import Decimal
from cars.models import Brand, BodyType, CarClass, CarModel, CarVariant

def make_brand(**kwargs) -> Brand:
    """Tạo Brand với giá trị mặc định, cho phép override."""
    defaults = dict(name="Toyota", country_of_origin="Japan")
    defaults.update(kwargs)
    return Brand.objects.create(**defaults)
 
 
def make_body_type(name="SUV") -> BodyType:
    return BodyType.objects.get_or_create(name=name, defaults={"slug": name.lower()})[0]
 
 
def make_car_class(name="Hạng D") -> CarClass:
    return CarClass.objects.get_or_create(name=name, defaults={"slug": "hang-d"})[0]
 
 
def make_car_model(brand=None, **kwargs) -> CarModel:
    if brand is None:
        brand = make_brand()
    defaults = dict(brand=brand, name="Camry")
    defaults.update(kwargs)
    return CarModel.objects.create(**defaults)
 
 
def make_variant(car_model=None, **kwargs) -> CarVariant:
    if car_model is None:
        car_model = make_car_model()
    defaults = dict(
        car_model=car_model,
        variant_name="2.5Q",
        fuel_type="gasoline",
        price_min=Decimal("1100"),
        price_max=Decimal("1200"),
    )
    defaults.update(kwargs)
    return CarVariant.objects.create(**defaults)
 