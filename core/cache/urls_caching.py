from functools import lru_cache
from core.helpers import CoreHelper

class CacheUrl:
    
    @classmethod
    @lru_cache(maxsize=1)
    def domain(cls):
        return CoreHelper.get_site_domain()
    
    
    @classmethod
    def brand_urls(cls, brand):
        d = cls.domain()
        urls = [
            f"{d}{brand.get_absolute_url()}",
            f"{d}/brands/",
            f"{d}/"
        ]
        return urls
    
    @classmethod
    def car_urls(cls, car_model):
        d = cls.domain()

        urls = [
            f"{d}{car_model.get_absolute_url()}",
            f"{d}/brands/{car_model.brand.slug}/",
            f"{d}/cars/",
            f"{d}/"
        ]
        return urls
        
    @classmethod
    def variant_urls(cls, variant):
        d = cls.domain()

        urls = [
            f"{d}{variant.get_absolute_url()}",
            f"{d}/cars/{variant.car_model.slug}/",
            f"{d}/brands/{variant.car_model.brand.slug}/",
            f"{d}/"
        ]
        return urls
    
    @classmethod
    def spec_urls(cls, spec):
        variant = spec.variant
        d = cls.domain()
        
        urls = [
            f"{d}{variant.get_absolute_url()}",
        ]
        return urls
    
    @classmethod
    def review_urls(cls, review):
        d = cls.domain()
        
        car_model = review.car
        variants = car_model.variants.filter(is_active=True)
        variant_urls = [f"{d}{variant.get_absolute_url()}" for variant in variants]
        urls = [
            f"{d}{car_model.get_absolute_url()}",
            *variant_urls,
            f"{d}/",
        ]
        return urls
    
    @classmethod
    def post_urls(cls, post):
        d = cls.domain()
        
        urls = [
            f"{d}{post.get_absolute_url()}",
            f"{d}/blogs/",         
            f"{d}/",               
        ]
        return urls

    @classmethod
    def brand_hist_urls(cls, brand_hist):
        d = cls.domain()
        
        urls = [
            f"{d}{brand_hist.get_absolute_url()}",
            f"{d}/brands/{brand_hist.brand.slug}/",         
                        
        ]
        return urls