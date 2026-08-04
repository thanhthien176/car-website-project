class CacheKeys:
    
    @staticmethod
    def active_brands():
        return 'brand:list:active'
    
    @staticmethod
    def sidebar_brands():
        return 'sidebar:brands'
    
    @staticmethod
    def brand_detail(slug):
        return f'brand:detail:{slug}'
    
    @staticmethod
    def car_models_of_brand(slug):
        return f'brand:detail:{slug}:car_models'
    
    @staticmethod
    def car_models_default():
        return f'car:list:default'
    
    @staticmethod
    def sidebar_body():
        return f'sidebar:body:types'
    
    @staticmethod
    def car_model_detail(slug):
        return f'car_model:detail:{slug}'
    
    @staticmethod
    def variants_of_car_model(slug):
        return f'car_model:detail:{slug}:variants'
    
    @staticmethod
    def reviews_of_car_model(slug):
        return f'car_model:detail:{slug}:reviews'
    
    @staticmethod
    def get_variant_detail(slug):
        return f'variant:detail:{slug}'
    
    @staticmethod
    def other_variants(slug):
        return f'variant:detail:{slug}:other_variants'
    
    @staticmethod
    def variant_spec_tabs(slug: str):
        return f"variant_spec_tabs:{slug}"