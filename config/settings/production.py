# config/settings/production.py

from django.conf.global_settings import ADMINS, SERVER_EMAIL

from .base import *
from decouple import config, Csv

DEBUG = False

SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Whitenoise
MIDDLEWARE = MIDDLEWARE[:1]+['whitenoise.middleware.WhiteNoiseMiddleware'] + MIDDLEWARE[1:]

INSTALLED_APPS += ['storages']
    
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':     config('DB_NAME'),
        'USER':     config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST':     config('DB_HOST', default='localhost'),
        'PORT':     config('DB_PORT', default='5432'),
        'CONN_MAX_AGE': 60,
    }
}

REDIS_HOST = config("REDIS_HOST", default="redis")
REDIS_PORT = config("REDIS_PORT", default=6379, cast=int)
REDIS_DB = config("REDIS_DB", default=1, cast=int)

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
        "TIMEOUT": 300,
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"

#=========S3 Storage==============
AWS_ACCESS_KEY_ID = config('R2_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('R2_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('R2_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = config('R2_ENDPOINT_URL')
AWS_S3_CUSTOM_DOMAIN = config('R2_PUBLIC_DOMAIN')
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'auto'
AWS_QUERYSTRING_AUTH = False

# Cloudflare purge caching
CLOUDFLARE_PURGE_ENABLED = config('CLOUDFLARE_PURGE_ENABLED', default=True, cast=bool)

# ── Security headers ────────────────────────────────────────────────────────
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Tells Django to trust the X-Forwarded-Proto header from Nginx.
# Without this, SECURE_SSL_REDIRECT causes an infinite redirect loop
# because Django sees HTTP (from Nginx) even though the original request was HTTPS.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ── Email ───────────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
ADMINS = [
    ("Thien", config("ADMIN_EMAIL")),
]
SERVER_EMAIL = config("EMAIL_HOST_USER")