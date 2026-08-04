from django.core.cache import cache
from django.shortcuts import get_object_or_404

from cars.services.model_services import SpecService
from core.cache.keys import CacheKeys

class SpecCacheService:
    TIMEOUT = None
    
    @classmethod
    def get_spec_tabs(cls, variant):
        key = CacheKeys.variant_spec_tabs(variant.slug)
        cached = cache.get(key)
        if cached is not None:
            return cached
        
        tabs = SpecService.get_spec_tabs(variant)
        cache.set(key, tabs, timeout=cls.TIMEOUT)
        return tabs