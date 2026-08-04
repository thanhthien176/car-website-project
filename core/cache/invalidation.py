from django.core.cache import cache

from core.cache.keys import CacheKeys


class ClearCacheKeys:
    
    @staticmethod
    def clear_brand_cache(brand):
        cache.delete_many([
            CacheKeys.active_brands(),
            CacheKeys.brand_detail(brand.slug),
            CacheKeys.sidebar_brands(),
            CacheKeys.car_models_of_brand(brand.slug),
            CacheKeys.car_models_default()
        ])
    
    @staticmethod
    def clear_car_model_cache(car_model):
        cache.delete_many([
            CacheKeys.car_models_of_brand(car_model.brand.slug),
            CacheKeys.car_model_detail(car_model.slug),
            CacheKeys.car_models_default(),
            CacheKeys.reviews_of_car_model(car_model.slug),
            CacheKeys.variants_of_car_model(car_model.slug),
        ])
        
    @staticmethod
    def clear_variant_cache(variant):
        cache.delete_many([
            CacheKeys.variants_of_car_model(variant.car_model.slug),
            CacheKeys.get_variant_detail(variant.slug),
            CacheKeys.other_variants(variant.slug),
            CacheKeys.variant_spec_tabs(variant.slug),
        ])
        
    @staticmethod
    def clear_body_type_cache(body_type):
        cache.delete_many([
            CacheKeys.sidebar_body(),
            CacheKeys.car_models_default(),
        ])
        
    @staticmethod
    def clear_review_cache(review):
        cache.delete_many([
            CacheKeys.car_model_detail(review.car.slug),
            CacheKeys.get_variant_detail(review.car.slug)
        ])
    
    @staticmethod
    def clear_spec_cache(variant):
        cache.delete_many([
            CacheKeys.variant_spec_tabs(variant.slug),
        ])   
    
    