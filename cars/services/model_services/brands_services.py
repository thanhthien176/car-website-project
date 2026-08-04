from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import get_object_or_404

from core.cache.keys import CacheKeys

class BrandService:


    CACHE_TTL = 24*60*60 # one day

    @classmethod
    def get_active_brands(cls):
        key = CacheKeys.active_brands()
        
        brands = cache.get(key)
        
        if brands is None:
            from cars.models import Brand
                
            brands = list(
                        Brand.objects
                        .filter(is_active=True)
                        .annotate(model_count=Count('car_models', distinct=True))
                        .order_by('name')
                    )
            cache.set(key, brands, cls.CACHE_TTL)
        
        return brands

    @classmethod
    def get_brand_detail(cls, slug, queryset=None):
        if queryset is None:
            from cars.models import Brand
            
            queryset = Brand.objects.filter(is_active=True)
            
        key = CacheKeys.brand_detail(slug)
        brand = cache.get(key)
        
        if brand is None:
            brand = get_object_or_404(queryset, slug=slug)
            cache.set(key, brand, cls.CACHE_TTL)
        return brand   

    @classmethod
    def get_car_models_brand(cls, brand):
        key = CacheKeys.car_models_of_brand(brand.slug)
        car_models = cache.get(key)
        if car_models is None:
            car_models = list(
                brand.car_models
                .select_related('body_type', 'car_class')
                .prefetch_related('variants')
                .order_by('name')
            )
            cache.set(key, car_models, cls.CACHE_TTL)
        return car_models 

        
        