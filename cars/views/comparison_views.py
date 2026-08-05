from typing import Any

from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

from cars.models import Comparison, CarVariant, CarModel
from cars.services.model_services import SpecService

def _get_or_create_comparison(request):
    """
    Helper: ensure session exists, then get or create 
    the Comparison tied to this session.
    Returns (comparison, session_key)
    """
    if not request.session.session_key:
        request.session.create()
        
    session_key = request.session.session_key
    comparison, _ = Comparison.objects.get_or_create(session_key=session_key)
    return comparison

def _render_tray(request, comparison, status):
    """Render comparison tray fragment để HTMX swap vào DOM."""
    cars = comparison.cars.select_related(
        'car_model__brand'
    ).prefetch_related('variant_images')
    total = cars.count()
    
    return render(request, "cars/comparison/_comparison_tray.html", {
        'comparison_cars': cars,
        'status': status,
        'can_add': comparison.can_add_car(),
        'total': total,
        'empty_slots': range(3-total),
    }
    )
    
class ComparisonPageView(TemplateView):
    template_name = 'cars/comparison/comparison_page.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        comparison = _get_or_create_comparison(self.request)
        
        spec_accessors = [name for name, _ in SpecService.get_spec_relations()]
        
        variants = list(
            comparison.cars
            .select_related(
                'car_model__brand',
                'car_model__body_type',
                'car_model__car_class'
            )
            .prefetch_related(
                'variant_images', *spec_accessors
            )
        )
        context['variants'] = variants
        context['comparison_tabs'] = SpecService.get_comparison_tabs(variants)
        return context


class AddToComparisonView(View):
    def post(self, request, variant_pk):
        comparison = _get_or_create_comparison(request)
        variant = get_object_or_404(CarVariant, pk=variant_pk, is_active=True)
        
        if comparison.cars.filter(pk=variant_pk).exists():
            status = "already_added"
        elif not comparison.can_add_car():
            status = "limit_reached"
        else:
            comparison.cars.add(variant)
            status = "added"
        
        return _render_tray(request, comparison, status)
    
class RemoveFromComparisonView(View):
    def post(self, request, variant_pk):
        comparison = _get_or_create_comparison(request)
        comparison.cars.remove(variant_pk)
        return _render_tray(request, comparison, "removed")
    
class ComparisonTrayView(View):
    """Serve tray HTML khi trang load — dùng cho hx-trigger='load'."""
    def get(self, request):
        comparison = _get_or_create_comparison(request)
        return _render_tray(request, comparison, status='init')
    
class VariantPickerView(View):
    """
    GET /cars/<model_slug>/variants/
    Return HTML fragment list variants of model,
    use HTMX swap into dropdown in car_list.
    """
    def get(self, request, slug):
        car_model = get_object_or_404(CarModel, slug=slug)
        variants = (
            car_model.variants
            .filter(is_active=True)
            .order_by('price_min')
        )
        
        # Get current comparison to know variant added
        comparison = _get_or_create_comparison(request)
        added_pks = set(comparison.cars.values_list('pk', flat=True))
        
        for variant in variants:
            variant.is_in_comparison = variant.pk in added_pks
        
        return render(request, 'cars/comparison/_variant_picker.html', {
            'car_model': car_model,
            'variants': variants,
            'added_pks': added_pks,
            'can_add': comparison.can_add_car(),
        })
        
class VariantPickerCloseView(View):
    def get(self, request, slug):
        # Return an empty div replaces the picker — effectively "closing" the dropdown
        return HttpResponse(f'<div id=f"picker-{slug}"></div>')

class ClearComparisonView(View):
    pass 