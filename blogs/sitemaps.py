from django.contrib.sitemaps import Sitemap
from blogs.models import BrandHistory, BlogPost

class BrandHistorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return BrandHistory.objects.filter(is_published=True).order_by('-updated_at')
    
    def location(self, obj) -> str:
        return obj.get_absolute_url()
    
    def lastmod(self, obj):
        return obj.updated_at
    
    
class BlogPostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return BlogPost.objects.filter(is_published=True).order_by('updated_at', 'created_at')
    
    def location(self, obj) -> str:
        return obj.get_absolute_url()
    
    def lastmod(self, obj):
        return obj.updated_at