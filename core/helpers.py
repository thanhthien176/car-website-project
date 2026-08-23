from django.contrib.sites.models import Site
from django.conf import settings

class CoreHelper:

    @classmethod
    def get_site_domain(cls):
        try:
            domain_name = Site.objects.get_current().domain
        except Exception:
            domain_name = getattr(settings, "SITE_DOMAIN", "xehoi360.com.vn")
        
        domain_name = domain_name.replace("https://", "").replace("http://", "").strip("/")
        
        return f"https://{domain_name}"