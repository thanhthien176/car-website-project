from functools import lru_cache
from core.helpers import CoreHelper

class CacheUrl:
    
    @classmethod
    @lru_cache(maxsize=1)
    def domain(cls):
        return CoreHelper.get_site_domain()
    
    @classmethod
    def brand_urls(cls, brand):
        urls = [
            f"{cls.domain}{brand.get_absolute_url()}",
            f"{cls.domain}/brands/",
            f"{cls.domain}/"
        ]
        return urls
    
    @classmethod
    def car_urls(cls, car_model):
        urls = [
            f"{cls.domain}{car_model.get_absolute_url()}",
            f"{cls.domain}/brands/{car_model.brand.slug}/",
            f"{cls.domain}/cars/",
            f"{cls.domain}/"
        ]
        return urls
        
    @classmethod
    def variant_urls(cls, variant):
        urls = [
            f"{cls.domain}{variant.get_absolute_url()}",
            f"{cls.domain}/cars/{variant.car_model.slug}/",
            f"{cls.domain}/brands/{variant.car_model.brand.slug}/",
            f"{cls.domain}/"
        ]
        return urls
    
    @classmethod
    def spec_urls(cls, spec):
        variant = spec.variant
        urls = [
            f"{cls.domain}{variant.get_absolute_url}",
        ]
        return urls
    
    @classmethod
    def review_urls(cls, review):
        car_model = review.car
        variants = car_model.variants.filter(is_active=True)
        variant_urls = [f"{cls.domain}{variant.get_absolute_url()}" for variant in variants]
        urls = [
            f"{cls.domain}{car_model.get_absolute_url()}",
            *variant_urls,
            f"{cls.domain}/",
        ]
        return urls
    
    @classmethod
    def post_urls(cls, post):
        urls = [
            f"{cls.domain}{post.get_absolute_url()}",
            f"{cls.domain}/blogs/",         
            cls.domain + "/",               
        ]
        return urls

    @classmethod
    def brand_hist_urls(cls, brand_hist):
        urls = [
            f"{cls.domain}{brand_hist.get_absolute_url()}",
            f"{cls.domain}/brands/{brand_hist.brand.slug}/",         
                        
        ]
        return urls