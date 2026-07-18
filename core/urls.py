from django.urls import path
from core.views import TermsView, DisclaimerView, PrivacyView, ContactView, AboutView

app_name = 'core'

urlpatterns = [
    path('general_term/', TermsView.as_view(), name="general_term"),
    path('privacy_policy/', PrivacyView.as_view(), name="privacy_policy"),
    path('disclaimer/', DisclaimerView.as_view(), name="disclaimer"),
    path('about-me/', AboutView.as_view(), name="about_me"),
    path('contact/', ContactView.as_view(), name="contact")
]