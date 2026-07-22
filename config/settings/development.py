# config/settings/development.py

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# In development, print emails to console instead of sending
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'