from django.db.models import Count, Min, Max, QuerySet

from cars.services.model_services.car_selector import CarSelector


class CarQueryService:
    
    @staticmethod
    def base_queryset() -> QuerySet:
        from cars.models import CarModel
        
        return (
            CarModel.objects
            .annotate(
                price_min=Min('variants__price_min'),
                price_max=Max('variants__price_max'),
            )
            .select_related(
                'brand',
                'body_type',
                'car_class',
            )
            .prefetch_related('images')
            .order_by('brand__name', 'name')
        )
        
    @staticmethod
    def filtered_queryset(params) -> QuerySet:
        """
        params: self.request.GET
        """
        qs = CarQueryService.base_queryset()
        
        selector = CarSelector()
        
        q = params.get('q', '').strip()
        
        if q:
            qs = selector.search_car_models(q, qs)
            
        qs = selector.apply_filters(qs,params)
        
        return qs.annotate(
            variant_count=Count('variants', distinct=True)
        )
        
    @staticmethod
    def detail_queryset() -> QuerySet:
        from cars.models import CarModel
        
        return (
            CarModel.objects
            .select_related('brand', 'body_type', 'car_class',)
            .prefetch_related('images')
        )
        
    @staticmethod
    def get_variants_of_car_model(car_model, params)-> QuerySet:
        """
        car_model: CarModel object
        params: self.request.user
        return QuerySet
        """
        return (
            car_model.variants # type: ignore
            .filter(is_active=True)
            .annotate_saved(params)  # AnonymousUser → False
            .prefetch_related('variant_images')
            .order_by('price_min')
        )
        
    @staticmethod
    def get_reviews_of_car_model(car_model) -> QuerySet:
        """
        car_model: CarModel object
        """
        return (
            car_model.reviews
            .filter(is_approved=True)
            .order_by('-created_at')[:10]
        )