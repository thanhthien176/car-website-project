# blogs/signals.py (hoặc thêm vào signals.py hiện có của bạn)
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction

from core.cache.cloudflare import CloudflareCacheService
from core.cache.urls_caching import CacheUrl
from blogs.models import BlogPost, BrandHistory

# Signal BlogPost
@receiver(post_save, sender=BlogPost)
@receiver(post_delete, sender=BlogPost)
def purge_cloudflare_on_post_change(sender, instance, **kwargs):
    urls = CacheUrl.post_urls(instance)
    transaction.on_commit(lambda: CloudflareCacheService.purge_urls(urls))


# Signal BrandHistory
@receiver(post_save, sender=BrandHistory)
@receiver(post_delete, sender=BrandHistory)
def purge_cloudflare_on_history_change(sender, instance, **kwargs):
    urls = CacheUrl.brand_hist_urls(instance)
    transaction.on_commit(lambda: CloudflareCacheService.purge_urls(urls))