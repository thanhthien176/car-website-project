
from cars.models import CarVariant

class VariantQueryService:
    
    @staticmethod
    def get_variant_detail(params):
        """
        params: self.request.user
        """
        return (
            CarVariant.objects
            .annotate_saved(params)
            .select_related(
                'car_model__brand',
                'car_model__body_type',
                'car_model__car_class',
            )
            .prefetch_related(
                'variant_images',
                'car_model__images',
                'engine',
                'dimension',
                'safety',
                # 'car_model__reviews',
            )            
        )
    