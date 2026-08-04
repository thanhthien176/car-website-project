from typing import Any

from django.views.generic import ListView, DetailView
from django.core.cache import cache

from cars.models import Brand
from cars.services.model_services import BrandService

class BrandListView(ListView):
    """
    Display all active brands in alphabetical order.
    Annotates each brand with model_count to avoid N+1 queries.
    """
    model = Brand
    template_name = 'cars/brands/brand_list.html'
    context_object_name = 'brands'
        
    def get_queryset(self):
       
        return BrandService.get_active_brands()
        

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
    
    
    def get_queryset(self):
        
        return Brand.objects.filter(is_active=True)
    
    def get_object(self, queryset=None) -> Any:
        slug = self.kwargs[self.slug_url_kwarg]
        return BrandService.get_brand_detail(slug, queryset)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        context['car_models'] = BrandService.get_car_models_brand(self.object)
        return context