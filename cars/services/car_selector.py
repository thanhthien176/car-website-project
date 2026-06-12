from typing import Any

from django.db.models import Count, Q
from cars.models import Brand, CarModel, CarVariant

class CarSelector:
    """
    Service layer for querying car-related data.
    Keeps views thin and business logic testable in isolation.
    """
    def get_featured_brands(self, limit: int = 8):
        """
        Return active brands with model_count annotation to avoid N+1.
        Template use {{ brand.model_count }} instead of {{ brand.car_models.count }}
        """
        return (Brand.objects
                .filter(is_active=True)
                .annotate(model_count=Count('car_models', distinct=True))
                .order_by("name")[:limit]
                )
        
    def get_latest_variants(self, limit: int = 6):
        """
        Return the most recently added active variants.
        select_related: fetch ForeignKey relations in a single JOIN query.
        prefetch_related: fetch reverse FK (images) in a separate query,
                          then Python-merge — avoids N+1 on M2M/reverse FK.
        """
        return (CarVariant.objects
                .filter(is_active=True)
                .select_related('car_model__brand', 'car_model__body_type')
                .prefetch_related('variant_images')
                .order_by('-id')[:limit]
                )
        
    def get_top_rated_models(self, limit: int = 4):
        """Return car models with highest average rating."""
        return (CarModel.objects
                .filter(avg_rating__gt=0)
                .select_related('brand')
                .order_by('-avg_rating')[:limit]
                )
        
    def search_car_models(self, query:str, qs=None):
        """
        Search active CarModels accross mutiple text fields.
        User OR logic: match any field -> include in results.
        
        .distinct() is required because the JOIN on car_model__body_type or car_model__car_class
        can produce duplicate rows when multiple field match

        Args:
            query (str): the key is what user want to search
        """
        if qs is None:
            qs = CarModel.objects.select_related("brand", "body_type", "car_class")
        
        if not query or not query.strip():
            return qs
        
        q = query.strip()
        return (
            qs.filter(
                Q(name__icontains=q) |
                Q(brand__name__icontains=q) |
                Q(description__icontains=q) |
                Q(body_type__name__icontains=q) |
                Q(car_class__name__icontains=q) |
                Q(variants__variant_name__icontains=q, variants__is_active=True)            
            )
            .select_related(
                'brand',
                'body_type',
                'car_class',
            )
            .prefetch_related('variants', 'images')
            .distinct()
            .order_by('brand__name', 'name')
        )
        
        
    def apply_filters(self, qs, params):
        qs = self._filter_brand(qs, params)
        qs = self._filter_body(qs, params)
        qs = self._filter_fuel(qs, params)
        qs = self._filter_price(qs, params)
        qs = self._filter_engine(qs, params)
        
        return qs
    
    def _filter_brand(self, qs, params):
        brand = params.get('brand')
        
        if brand:
            qs = qs.filter(
                brand__slug=brand
            )
        return qs
    
    def _filter_body(self, qs, params):
        body = params.get('body')
        
        if body:
            qs = qs.filter(
                body_type__slug=body
            )
        return qs
    
    def _filter_fuel(self, qs, params):
        fuel = params.get('fuel')
        
        if fuel:
            qs = qs.filter(
                variants__fuel_type=fuel,
                variants__is_active=True,
            )
        return qs
    
    def _filter_price(self, qs, params):
        min_price = self._to_int(
            params.get('min_price')
        )
        max_price = self._to_int(
            params.get('max_price')
        )
        
        if min_price is None and max_price is None:
            return qs
        
        filters: dict[str, Any] = {
            "variants__is_active": True
        }
        
        if min_price is not None:
            filters["variants__price_min__gte"] = min_price * 1_000_000
        
        if max_price is not None:
            filters["variants__price_min__lte"] = max_price * 1_000_000
            
        return qs.filter(**filters).distinct()
    
    def _filter_engine(self, qs, params):
        key = params.get('engine')
        
        if key:
            pass
        
        return qs
    
    def _to_int(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
        