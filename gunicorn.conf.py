import multiprocessing

# ---------------------------------------------------------------------------
# Server socket
# ---------------------------------------------------------------------------

# Bind to localhost only — Nginx will proxy requests to this address.
# Never bind 0.0.0.0 in production unless Nginx is on a separate machine.
bind = "127.0.0.1:8000"

# ---------------------------------------------------------------------------
# Worker processes
# ---------------------------------------------------------------------------

# Formula: (2 x CPU cores) + 1
# VPS: 2 cores → 5 workers
workers = multiprocessing.cpu_count()*2 + 1

# Sync workers (default): one request at a time per worker, simple and stable.
# Switch to "gevent" or "uvicorn.workers.UvicornWorker" only when async is needed.
worker_class = "sync"

# Kill and respawn a worker if it does not respond within this many seconds.
# Set to 60s: validator limits uploads to 5MB, WebP conversion should finish well within 1 minute.
# Future: migrate image processing to Celery to remove this constraint entirely.
timeout = 60

# Graceful timeout: how long to wait for workers to finish current requests
# before force-killing during a reload/shutdown.
graceful_timeout = 30

# ---------------------------------------------------------------------------
# Memory management
# ---------------------------------------------------------------------------

# Load the Django application in the master process before forking workers.
# Workers inherit the loaded app via copy-on-write, reducing total RAM usage.
# Trade-off: DB connections opened before fork are shared — Django handles this
# correctly by reopening connections per-worker after fork.
preload_app = True

# Restart a worker after it has served this many requests.
# Prevents slow memory leaks from accumulating indefinitely.
max_requests = 1000
max_requests_jitter = 100   # randomize restart to avoid all workers restarting simultaneously

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

accesslog = "logs/gunicorn_access.log"
errorlog = "logs/gunicorn_error.log"
loglevel = "info"

# Forward access logs to Django's logging system as well.
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
