from django.http import JsonResponse
from django.db import connection, OperationalError
from django.core.cache import cache

def health_check(request):
    """
    Lightweight health check endpoint.
    No authentication required - monitoring tools need auauthenticated access.
    Returns 200 if all critical services operational, 503 if database down.
    """
    checks = {}
    http_status = 200
    
    # Database: critical - app cannot function without it
    try:
        connection.ensure_connection()
        checks["database"] = "ok"
    except OperationalError as exc:
        checks["database"] = f"Error {exc}"
        http_status = 503
        
    # Cache: non-critical - app degrades gracefully without it
    try:
        cache.set("health_ping", "pong", timeout=10)
        checks["cache"] = "ok" if cache.get("health_ping") == "pong" else "miss"
    except Exception as exc:
        checks["cache"] = f"warning: {exc}"
    
    
    return JsonResponse({
        "status": "healthy" if http_status == 200 else "unhealthy",
        "checks": checks,
    }, status=http_status)