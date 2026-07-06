from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.views import View

from cars.models import CarVariant
from users.models import SavedCar

class ToggleSavedCarView(LoginRequiredMixin, View):
    """
    HTMX endpoint: toggle save/unsave a CarVariant for the current user.
    Returns only the button fragment — HTMX swaps it in place.
    """
    
    
    def post(self, request, variant_pk):
        variant = get_object_or_404(CarVariant, pk=variant_pk, is_active=True)
        
        saved_qs = SavedCar.objects.filter(user=request.user, car=variant)
        if saved_qs.exists():
            saved_qs.delete()
            variant.is_saved=False
        else:
            SavedCar.objects.create(user=request.user, car=variant)
            variant.is_saved=True
            
        html = render_to_string(
            "utils/_saved_car_button.html",
            {'variant': variant},
            request=request,
        )
        return HttpResponse(html)
        
    