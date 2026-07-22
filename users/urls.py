from django.urls import path
from users.views import ProfileUpdateView, ProfileView, ToggleSavedCarView, ResendConfirmationEmailView

app_name ="users"

urlpatterns = [
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('saved-cars/<int:variant_pk>/toggle', ToggleSavedCarView.as_view(), name="toggle_saved_car"),
    path('resend-confirmation/', ResendConfirmationEmailView.as_view(), name='resend_confirmation'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
]

