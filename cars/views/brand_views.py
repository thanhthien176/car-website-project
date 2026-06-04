from typing import Any

from django.db.models import Count, QuerySet
from django.views.generic import ListView, DetailView

from cars.models import Brand

class BrandListView(ListView):
    """
    Display all active brands in alphabetical order.
    Annotates each brand with model_count to avoid N+1 queries.
    """
    model = Brand
    template_name = 'cars/brands/brand_list.html'
    context_object_name = 'brands'
    
    def get_queryset(self) -> QuerySet:
        return (Brand.objects
                .filter(is_active=True)
                .annotate(model_count=Count('car_models', distinct=True))
                .order_by('name')
                )
        

class BrandDetailView(DetailView):
    """
    Show a single brand's detail page with its car models.
    Slug-based lookup for SEO-friendly URLs.
    """
    model = Brand
    template_name = 'cars/brands/brand_detail.html'
    context_object_name = 'brand'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self) -> QuerySet:
        return Brand.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['car_models']=(
            self.object.car_models
            .select_related('body_type', 'car_class')
            .prefetch_related('variants')
            .order_by('name')
        )
        return context