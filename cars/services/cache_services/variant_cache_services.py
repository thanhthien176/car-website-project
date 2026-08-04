from django.core.cache import cache
from django.shortcuts import get_object_or_404

from cars.services.model_services import CarQueryService
from core.cache.keys import CacheKeys

class VariantCacheService:
    
    CACHE_TTL = 24*60*60
    
    @classmethod
    def get_variant_detail(cls, queryset, slug):
        key = CacheKeys.get_variant_detail(slug)
        variant = cache.get(key)
        
        if variant is None:
            variant = get_object_or_404(queryset, slug=slug)
            cache.set(key, variant, cls.CACHE_TTL)
        
        return variant
    
    @staticmethod
    def get_other_variant(car_model, slug, user):
        key = CacheKeys.other_variants(slug)
        other_variants = cache.get(key)
        
        if other_variants is None:
            other_variants = list(
                    CarQueryService
                    .get_variants_of_car_model(car_model, user)
                    .exclude(slug=slug)
                    )
            cache.set(key, other_variants, timeout=None)
        
        return other_variants
    
    