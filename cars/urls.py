from django.urls import path
from cars.views.home import HomeView
from cars.views.brand_views import BrandListView, BrandDetailView
from cars.views.cars_views import CarModelListView, CarModelDetailView, CarVariantDetailView
from cars.views.review_views import ReviewSubmitView
from cars.views.comparison_views import (ComparisonPageView, AddToComparisonView, 
                                         RemoveFromComparisonView, ClearComparisonView,
                                         VariantPickerCloseView, VariantPickerView,
                                         ComparisonTrayView)
from blogs.views import BrandHistoryView

app_name = 'cars'

urlpatterns = [
    path('', HomeView.as_view(), name='home' ),
    
    # brands
    path('brands/', BrandListView.as_view(), name='brand_list'),
    path('brands/<slug:slug>/', BrandDetailView.as_view(), name='brand_detail'),
    path('brands/<slug:slug>/history/', BrandHistoryView.as_view(), name="brand_history"),
    
    # cars
    path('cars/', CarModelListView.as_view(), name='car_list'),
    path('cars/<slug:slug>/', CarModelDetailView.as_view(), name='car_detail'),
    path('cars/<slug:slug>/picker/', VariantPickerView.as_view(), name='variant_picker'),
    path('cars/<slug:slug>/picker/close/', VariantPickerCloseView.as_view(), name='variant_picker_close'),
    path('variants/<slug:slug>/', CarVariantDetailView.as_view(), name='variant_detail'),
    path('cars/<slug:slug>/review/', ReviewSubmitView.as_view(), name='review_submit'),
    
    # comparison
    path('comparison/', ComparisonPageView.as_view(), name='comparison_page'),
    path('comparison/tray/', ComparisonTrayView.as_view(), name='comparison_tray'),
    path('comparison/add/<int:variant_pk>/', AddToComparisonView.as_view(), name='comparison_add'),
    path('comparison/remove/<int:variant_pk>/', RemoveFromComparisonView.as_view(), name='comparison_remove'),
    path('comparison/clear/', ClearComparisonView.as_view(), name='comparison_clear'),
    
]
