from random import choice

import django_filters
from cars.models import CarVariant, CarModel

class CarModelFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(
        field_name='brand__slug',
        lookup_expr='exact',
        label='Brand slug',
    )
    body=django_filters.CharFilter(
        field_name='body_type__slug',
        lookup_expr='exact',
        label='Body type slug'
    )

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
    
    body = django_filters.CharFilter(
        field_name='car_model__body_type__slug',
        lookup_expr='exact',
        label='Body Type slug',
    )
    
    fuel_type = django_filters.ChoiceFilter(
        choices=CarVariant.FUEL_TYPE_CHOICES
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
    