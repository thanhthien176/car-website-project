from typing import Any

from django.db.models import QuerySet, Count
from django.views.generic import ListView, DetailView
from ..models import CarModel, CarVariant

class CarModelListView(ListView):
    """list car models, supports optional ?brand=<slug> filter

    Args:
        ListView (_type_): _description_
    """
    model = CarModel
    template_name = "cars/car_list.html"
    context_object_name = "car_models"
    paginate_by = 12
    
    def get_queryset(self) -> QuerySet:
        qs = (CarModel.objects
              .select_related("brand", "body_type", "car_class")
              .annotate(variant_count=Count('variants'))
              .order_by("brand__name", "name")
              )
        brand_slug = self.request.GET.get('brand')
        if brand_slug:
            qs = qs.filter(brand__slug=brand_slug)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass current filter back to template for active state UI
        context['current_brand'] = self.request.GET.get('brand', '')
        return context
    
    
class CarVariantDetailView(DetailView):
    """
    Full detail page for a single CarVariant.
    Prefetches all related specs and images.
    """
    model = CarVariant
    template_name = 'cars/variant_detail.html'
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