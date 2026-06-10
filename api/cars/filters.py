import django_filters
from cars.models import CarVariant

class CarVariantFilter(django_filters.FilterSet):
    """
    Custom FilterSet for CarVariant with price range support.

    Supported query params:
        ?fuel_type=hybrid
        ?is_active=true
        ?brand=toyota          (brand slug)
        ?price_min=500000000   (price_min >= value)
        ?price_max=1000000000  (price_max <= value)
    """
    # Traverse FK: filter by brand slug on the related CarModel → Brand
    brand = django_filters.CharFilter(
        field_name='car_model__brand__slug',
        lookup_expr='exact',
        label='Brand slug',
    )
    
    body_type = django_filters.CharFilter(
        field_name='car_model__body_type__slug',
        lookup_expr='exact',
        label='Body Type slug',
    )
    # Price range: gte / lte instead of exact
    price_min = django_filters.NumberFilter(
        field_name='price_min',
        lookup_expr='gte',
        label='Price from (VND)',
    )
    price_max = django_filters.NumberFilter(
        field_name='price_max',
        lookup_expr='lte',
        label='Price to (VND)',
    )
    