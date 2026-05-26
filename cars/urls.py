from django.urls import path
from cars.views.home import HomeView

app_name = 'cars'

urlpatterns = [
    path('', HomeView.as_view(), name='home' ),
]
