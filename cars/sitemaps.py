from django.contrib.sitemaps import Sitemap
from cars.models import CarModel, CarVariant, Brand

class BrandSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return Brand.objects.filter(is_active=True).order_by('slug')
    
    def location(self, obj) -> str:
        return obj.get_absolute_url()
    
    def lastmod(self, obj):
        return obj.updated_at
    

class CarModelSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        return CarModel.objects.select_related('brand').order_by('slug')
    
    def location(self, obj):
        return obj.get_absolute_url()
    
    def lastmod(self, obj):
        return obj.updated_at
    
    
class CarVariantSitemap(Sitemap):
    changfreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return (
            CarVariant.objects
            .filter(is_active=True)
            .select_related('car_model__brand')
            .order_by('slug')
        )
    
    def location(self, obj) -> str:
        return obj.get_absolute_url() 
    
    def lastmod(self, obj):
            return obj.updated_at