from django.db.models import Count
from cars.models import Brand, CarModel, CarVariant

class CarSelector:
    """
    Service layer for querying car-related data.
    Keeps views thin and business logic testable in isolation.
    """
    def get_featured_brands(self, limit: int = 8):
        """
        Return active brands with model_count annotation to avoid N+1.
        Template use {{ brand.model_count }} instead of {{ brand.car_models.count }}
        """
        return (Brand.objects
                .filter(is_active=True)
                .annotate(model_count=Count('car_models', distinct=True))
                .order_by("name")[:limit]
                )
        
    def get_latest_variants(self, limit: int = 6):
        """
        Return the most recently added active variants.
        select_related: fetch ForeignKey relations in a single JOIN query.
        prefetch_related: fetch reverse FK (images) in a separate query,
                          then Python-merge — avoids N+1 on M2M/reverse FK.
        """
        return (CarVariant.objects
                .filter(is_active=True)
                .select_related('car_model__brand', 'car_model__body_type')
                .prefetch_related('images')
                .order_by('-id')[:limit]
                )
        
    def get_top_rated_models(self, limit: int = 4):
        """Return car models with highest average rating."""
        return (CarModel.objects
                .filter(avg_rating__gt=0)
                .select_related('brand')
                .order_by('-avg_rating')[:limit]
                )