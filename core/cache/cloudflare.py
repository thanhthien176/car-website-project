# core/cache/cloudflare

import logging
from django.contrib.messages import success
import requests
import atexit
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings

logger = logging.getLogger(__name__)

CLOUDFLARE_API_BASE = "https://api.cloudflare.com/client/v4"
MAX_URLS_PER_REQUEST = 30  # Cloudflare limit 30 URL/request (free/pro plan)

class CloudflareCacheService:
    """Purge Cloudflare edge cache cho zone xehoi360.com.vn."""
    _executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="cf-purge")
    atexit.register(_executor.shutdown, wait=False)
    
    
    @classmethod
    def _headers(cls):
        return {
            "Authorization": f"Bearer {settings.CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json",
        }
    
    @classmethod
    def _execute_purge(cls, json_payload: dict, log_label: str):
        """Function that executes the actual request (running on a background thread)."""
        if not settings.CLOUDFLARE_PURGE_ENABLED:
            return

        endpoint = f"{CLOUDFLARE_API_BASE}/zones/{settings.CLOUDFLARE_ZONE_ID}/purge_cache"
        
        try:
            resp = requests.post(
                endpoint,
                headers=cls._headers(),
                json=json_payload,
                timeout=10,
            )
            data = resp.json()
            if not data.get("success"):
                logger.error("Cloudflare %s failed: %s", log_label, data.get("errors"))
            else:
                logger.info("Cloudflare %s success: %s", log_label, json_payload)
        except Exception:
            logger.error("Cloudflare %s request error", log_label)
        
    
    @classmethod
    def purge_urls(cls, urls: list[str]):
        """
        Purge specific list of URLs (do not clear the entire cache).
        """
        if not urls:
            return
        
        endpoint = f"{CLOUDFLARE_API_BASE}/zones/{settings.CLOUDFLARE_ZONE_ID}/purge_cache"
        
        # Cloudflare limits the number of URLs per request -> use batching
        for i in range(0, len(urls), MAX_URLS_PER_REQUEST):
            batch = urls[i:i + MAX_URLS_PER_REQUEST]
            
            cls._executor.submit(
                cls._execute_purge,
                {"files": batch},
                f"purge_urls ({len(batch)} URLs)"
            )
        
    
    @classmethod
    def purge_everything(cls):
        """
        Purge the entire zone cache. Free/Pro plans are limited to approximately 500 requests per day.
        """
        
        cls._executor.submit(
            cls._execute_purge,
            {"purge_everything": True},
            "purge_everything"
        )
