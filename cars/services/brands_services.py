from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import get_object_or_404

from core.cache.keys import CacheKeys
from cars.models import Brand

CACHE_TTL = 24*60*60 # one day

def get_active_brands():
    key = CacheKeys.active_brands()
    
    brands = cache.get(key)
    
    if brands is None:    
        brands = list(
                    Brand.objects
                    .filter(is_active=True)
                    .annotate(model_count=Count('car_models', distinct=True))
                    .order_by('name')
                )
        cache.set(key, brands, CACHE_TTL)
    
    return brands

def get_brand_detail(slug, queryset=None):
    if queryset is None:
        queryset = Brand.objects.filter(is_active=True)
        
    key = CacheKeys.brand_detail(slug)
    brand = cache.get(key)
    
    if brand is None:
        brand = get_object_or_404(queryset, slug=slug)
        cache.set(key, brand, CACHE_TTL)
    return brand   


def get_car_models_brand(brand):
    key = CacheKeys.car_models_of_brand(brand.slug)
    car_models = cache.get(key)
    if car_models is None:
        car_models = list(
            brand.car_models
            .select_related('body_type', 'car_class')
            .prefetch_related('variants')
            .order_by('name')
        )
        cache.set(key, car_models, CACHE_TTL)
    return car_models 

    
    