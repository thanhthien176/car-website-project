# Minimal settings used ONLY during Docker build for `collectstatic`.
# This file intentionally has no database config, no secrets from .env —
# collectstatic does not need a DB connection or a real SECRET_KEY.

from .base import *

SECRET_KEY = "dummy-secret-key-for-build-time-only-not-used-at-runtime"

DEBUG = False

ALLOWED_HOSTS = ["*"]

# Static files — same storage backend as production
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}