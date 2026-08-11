"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap

from cars.sitemaps import BrandSitemap, CarModelSitemap, CarVariantSitemap
from cars.views.dashboard_view import admin_dashboard

from blogs.sitemaps import BrandHistorySitemap, BlogPostSitemap

from config.health import health_check


sitemaps = {
    'brands': BrandSitemap,
    'car_models': CarModelSitemap,
    'variants': CarVariantSitemap,
    'brand_histories': BrandHistorySitemap,
    'blog_posts': BlogPostSitemap,
}

urlpatterns = [
    path('cockpit/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('cockpit/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('', include('cars.urls')),
    path('blogs/', include('blogs.urls', namespace='blogs')),
    path('api/v1/', include('api.urls', namespace='api')),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('core/', include('core.urls', namespace='core')),
    
    
    
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain',
        ),
        name='robots_txt'
    ),
    path('sitemap.xml', 
         sitemap,
         {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path('health/', health_check, name="health_check"),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
