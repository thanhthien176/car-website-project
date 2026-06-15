from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count

from cars.models import Brand, CarModel, CarVariant
from .filters import CarVariantFilter, CarModelFilter
from .serializers import BrandSerializers, CarModelSerializers, CarVariantSerializers

class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for Brand
    Supports: list, retrive, search, ordering
    """
    serializer_class = BrandSerializers
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country_of_origin']
    ordering_fields = ['name', 'founded_year']
    ordering = ['name']
    
    def get_queryset(self):
        return (
            Brand.objects
            .filter(is_active=True)
            .annotate(car_model_count=Count('car_models', distinct=True))
        )
        
class CarModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API endpoint for CarModel.
    Supports: list, retrieve, filter by brand slug, search, ordering.
    """
    serializer_class = CarModelSerializers
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter ]
    filterset_class = CarModelFilter
    # filterset_fields = ['brand__slug','body_type__slug']
    search_fields = ['name', 'brand__name']
    ordering_filter = ['name', 'avg_rating', 'model_year']
    ordering = ['brand__name', 'name']
    
    def get_queryset(self):
        return (
            CarModel.objects
            .select_related('brand', 'body_type', 'car_class')
            .annotate(variant_count=Count('variants', distinct=True))
        )
        
class CarVariantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CarVariantSerializers
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['fuel_type', 'is_active', 'car_model__brand__slug']
    filterset_class = CarVariantFilter
    search_fields = ['name', 'car_model__name', 'car_mode__brand__name']
    ordering_fields = ['price_min', 'price_max', 'name']
    ordering = ['car_model__brand__name', 'name']
    
    def get_queryset(self):
        return (
            CarVariant.objects
            .filter(is_active=True)
            .select_related(
                'car_model__body_type',
                'car_model__brand')
            .prefetch_related('variant_images')
        )