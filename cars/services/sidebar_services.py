from django.core.cache import cache

from cars.models import BodyType, Brand
from core.cache.keys import CacheKeys

class SidebarService:
    CACHE_TTL = 24*60*60 # one day
    
    @staticmethod
    def brands():
        key = CacheKeys.sidebar_brands()
        
        return cache.get_or_set(
            key,
            lambda: list(Brand.objects.filter(is_active=True).order_by('name')),
            SidebarService.CACHE_TTL,
        )
        
    @staticmethod
    def body_types():
        key = CacheKeys.sidebar_body()
        return cache.get_or_set(
            key,
            lambda: list(BodyType.objects.order_by('name')),
            SidebarService.CACHE_TTL,
        )
        
        
        