from django.urls import path
from cars.views.home import HomeView
from cars.views.brand_views import BrandListView, BrandDetailView
from cars.views.cars_views import CarModelListView, CarModelDetailView, CarVariantDetailView
from cars.views.review_views import ReviewSubmitView

app_name = 'cars'

urlpatterns = [
    path('', HomeView.as_view(), name='home' ),
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/<slug:slug>/', BrandDetailView.as_view(), name='brand_detail'),
    path('cars/', CarModelListView.as_view(), name='car_list'),
    path('cars/<slug:slug>', CarModelDetailView.as_view(), name='car_detail'),
    path('variants/<slug:slug>/', CarVariantDetailView.as_view(), name='variant_detail'),
    path('cars/<slug:slug>/review', ReviewSubmitView.as_view(), name='review_submit')
]
