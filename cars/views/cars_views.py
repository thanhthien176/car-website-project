from typing import Any

from django.db.models import QuerySet
from django.core.cache import cache
from django.shortcuts import render
from django.views.generic import ListView, DetailView


from cars.models import CarModel, CarVariant
from cars.forms import ReviewForm
from cars.services.car_cache_services import CarCacheService
from cars.services.car_query_services import CarQueryService
from cars.services.sidebar_services import SidebarService
from cars.services.variant_query_services import VariantQueryService
from cars.services.variant_cache_services import VariantCacheService

class CarModelListView(ListView):
    """list car models, supports optional ?brand=<slug> filter

    Args:
        ListView (_type_): _description_
    """
    model = CarModel
    template_name = "cars/car_models/car_list.html"
    context_object_name = "car_models"
    paginate_by = 12
               
    
    def get_queryset(self) -> QuerySet:
        
        if car_models := CarCacheService.get_default(self.request.GET):
            return car_models
        
        qs = CarQueryService.filtered_queryset(self.request.GET)
                
        qs = CarCacheService.store_default(qs, self.request.GET, self.paginate_by)       
            
        return qs
    
    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any):
        if self.request.headers.get("HX-Request"):
            return render(self.request, 'cars/car_models/_car_grid.html', context )
        return super().render_to_response(context, **response_kwargs)
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        # Sidebar data
        context['all_brands'] = SidebarService.brands()
        context['all_body_types'] = SidebarService.body_types()
        
        # Preserve active filter state for template
        context['has_filters'] = CarCacheService.has_filter(self.request.GET)
        context['current_brand'] = self.request.GET.get('brand', '')
        context['current_body'] = self.request.GET.get('body', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context
    
class CarModelDetailView(DetailView):
    """
    Show a single CarModel with all its active variants.
    This is the "model page" - user picks a variant from here.
    """
    model = CarModel
    template_name = "cars/car_models/car_detail.html"
    context_object_name = "car_model"
    slug_url_kwarg = "slug"
    
    def get_queryset(self) -> QuerySet:
        return CarQueryService.detail_queryset()
    
    def get_object(self, queryset = None) -> Any:
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs[self.slug_url_kwarg]
        return CarCacheService.get_detail(slug, queryset)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            variants = list(CarQueryService.get_variants_of_car_model(self.object, self.request.user))
        else:
            qs = CarQueryService.get_variants_of_car_model(self.object, self.request.user)
            variants = CarCacheService.get_variants_of_car_model(self.object, qs)
        
        context['variants'] = variants
        context['form'] = ReviewForm()
        
        qs_review = CarQueryService.get_reviews_of_car_model(self.object)
        context['reviews'] = CarCacheService.get_reviews_of_car_model(self.object, qs_review)
        return context
    
class CarVariantDetailView(DetailView):
    """
    Full detail page for a single CarVariant.
    Prefetches all related specs and images.
    """
    model = CarVariant
    template_name = 'cars/variants/variant_detail.html'
    context_object_name = 'variant'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return VariantQueryService.get_variant_detail(self.request.user)
    
    def get_object(self, queryset=None) -> Any:
        if queryset is None:
            queryset = self.get_queryset()
        slug = self.kwargs[self.slug_url_kwarg]
        return  VariantCacheService.get_variant_detail(queryset, slug)
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        qs = CarQueryService.get_reviews_of_car_model(self.object.car_model)
        context['reviews'] = CarCacheService.get_reviews_of_car_model(self.object.car_model, qs)
        
        qs_other = (
                    CarQueryService
                    .get_variants_of_car_model(self.object.car_model, self.request.user)
                    .exclude(pk=self.object.pk)
                    )
        context['other_variants'] = VariantCacheService.other_variant(qs_other, self.object.slug)
            
           
        return context