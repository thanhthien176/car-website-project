from typing import Any

from django.db.models import QuerySet, Count
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from ..models import CarModel, CarVariant, Brand, BodyType
from cars.services.car_selector import CarSelector

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
        qs = (CarModel.objects
              .select_related("brand", "body_type", "car_class")
              .order_by("brand__name", "name")
              )
        brand_slug = self.request.GET.get('brand')
        body_slug = self.request.GET.get('body')
        if brand_slug:
            qs = qs.filter(brand__slug=brand_slug)
        if body_slug:
            qs = qs.filter(body_type__slug=body_slug)
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = CarSelector().search_car_models(q, qs=qs)
            
        return qs.annotate(variant_count=Count('variants', distinct=True))
    
    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any):
        if self.request.headers.get("HX-Request"):
            return render(self.request, 'cars/car_models/_car_grid.html', context )
        return super().render_to_response(context, **response_kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sidebar data
        context['all_brands'] = Brand.objects.filter(is_active=True).order_by('name')
        context['all_body_types'] = BodyType.objects.all().order_by('name')
        # Preserve active filter state for template
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
        return (
            CarModel.objects
            .select_related('brand', 'body_type', 'car_class')
        )
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['variants'] = (self.object.variants
                               .filter(is_active=True)
                               .prefetch_related('images')
                               .order_by('price_min')
                               )
        context['reviews'] = (self.object.reviews
                              .filter(is_approved=True)
                              .order_by('-created_at')[:5]
                              )
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
        return ( 
                CarVariant.objects
                .select_related(
                    'car_model__brand',
                    'car_model__body_type',
                    'car_model__car_class',
                )
                .prefetch_related(
                    'images',
                    'engine',
                    'dimension',
                    'safety',
                    'car_model__reviews'
                )            
        )
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['reviews'] = (
            self.object.car_model.reviews
            .filter(is_approved=True)
            .order_by('-created_at')[:10]
        )
        context['other_variants'] = (
            self.object.car_model.variants
            .exclude(pk=self.object.pk)
            .filter(is_active=True)
        )
        return context