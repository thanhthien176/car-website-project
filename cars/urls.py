from django.urls import path
from cars.views.home import HomeView
from cars.views.brand_views import BrandListView, BrandDetailView

app_name = 'cars'

urlpatterns = [
    path('', HomeView.as_view(), name='home' ),
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/<slug:slug>/', BrandDetailView.as_view(), name='brand_detail')
]
