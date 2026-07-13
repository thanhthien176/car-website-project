from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

from users.models import User
from users.forms import ProfileUpdateForm


class ProfileView(DetailView):
    """
    Public profile page — anyone can view.
    Looked up by username (unique field on User), not pk.
    """
    model = User
    template_name = "users/profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # Prefetch saved cars with related variant data to avoid N+1
        context["saved_cars"] = (
            self.object.saved_cars
            .select_related('car__car_model__brand')
            .order_by('-saved_at')
        )
        return context
    

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edit own profile. Always operates on request.user —
    ignores any object id from the URL to prevent IDOR.
    """
    model = User
    form_class = ProfileUpdateForm
    template_name = "users/profile_edit.html"
    
    def get_object(self, queryset: QuerySet | None = None) -> Any:
        return self.request.user
    
    def get_success_url(self) -> str:
        return reverse("users:profile", kwargs={"username": self.request.user.get_username()})
    
