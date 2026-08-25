from django.core.cache import cache
from django.shortcuts import get_object_or_404

from cars.services.model_services import CarQueryService
from core.cache.keys import CacheKeys


class CarCacheService:
    
    FILTERS = [
        'brand',
        'body',
        'min_price',
        'max_price',
    ]
    
    @classmethod
    def has_filter(cls, params):
        if params.get('q'):
            return True
        
        return any(
            params.get(k)
            for k in cls.FILTERS
        )

    @classmethod
    def is_first_page(cls, params):
        return params.get('page', '1') == '1'
    
    @classmethod
    def get_default(cls, params):
        """
        params: self.request.GET
        """
        has_filter = cls.has_filter(params)
        
        if not has_filter:
            key = CacheKeys.car_models_default()
            cached = cache.get(key)
            if cached:
                return cached
        return None
    
    @classmethod
    def store_default(cls, qs, params):
        has_filter = cls.has_filter(params)
        is_first_page = cls.is_first_page(params)
        
        if not has_filter and is_first_page:
            
            cache_ttl = 60*60
            key = CacheKeys.car_models_default()
            result = list(qs)
            
            cache.set(key, result, cache_ttl)
            return qs
        
        return qs
    
    @staticmethod
    def get_detail(slug, queryset):
                
        key = CacheKeys.car_model_detail(slug)
        car_model = cache.get(key)
        if car_model is None:
            car_model = get_object_or_404(queryset, slug=slug)
            cache.set(key, car_model, 60*60)
        return car_model
    
    @staticmethod
    def get_variants_of_car_model(car_model, qs):
        key = CacheKeys.variants_of_car_model(car_model.slug)
        variants = cache.get(key)
        if variants is None:
            variants = list(qs)
            cache.set(key, variants, 60*60)
        
        return variants
    
    @staticmethod
    def get_reviews_of_car_model(car_model, qs):
        key = CacheKeys.reviews_of_car_model(car_model.slug)
        reviews = cache.get(key)
        if reviews is None:
            reviews = list(qs)
            cache.set(key, reviews, 60*60)
        
        return reviews
        