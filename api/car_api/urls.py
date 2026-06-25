from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter
from .views import BrandViewSet, CarModelViewSet, CarVariantViewSet

router = DefaultRouter()
router.register('brands', BrandViewSet, basename='brand')
router.register('cars', CarModelViewSet, basename='car')
router.register('variants', CarVariantViewSet, basename='variant')

urlpatterns = router.urls

