# config/settings/base.py

from pathlib import Path
from decouple import config
from django.conf.global_settings import AUTH_USER_MODEL, AUTHENTICATION_BACKENDS, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL

from .logging_config import build_logging_config

# BASE_DIR must point up 2 levels because this file is in config/settings/
# config/settings/base.py → .parent = config/settings → .parent = config → .parent = project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent

LOGGING = build_logging_config(BASE_DIR)
SECRET_KEY = config('SECRET_KEY', default="django-insecure-build-secret-key")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django_extensions',
    'rest_framework',
    'django_filters',
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    # local apps
    'api',
    'cars',
    'blogs',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========Set AUTH_USER_MODEL===========
# Custom User model — must be set before any migration references User.
# Changing this after migrations exist requires dropping the entire database.
AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
}

ACCOUNT_FORMS = {
    "login": "users.forms.CustomLoginForm",
    "signup": "users.forms.CustomSignupForm",
}


# Encryption keys for sensitive fields (phone, cccd, address)
# Generate ENCRYPTION_KEY with:
# python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
ENCRYPTION_KEY = config("ENCRYPTION_KEY", default="")
ENCRYPTION_HASH_SALT = config("ENCRYPTION_HASH_SALT", default="")

# Required by django.contrib.sites
SITE_ID = 1

# ── django-allauth config ────────────────────────────────────────────────────
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django Admin
    'django.contrib.auth.backends.ModelBackend',
    # allauth specific authentication methods (social login, email)
    'allauth.account.auth_backends.AuthenticationBackend',    
]

ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_SIGNUP_FIELDS = ['email*', 'password1*', 'password2*' ]
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Xehoi360]'
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'

LOGIN_REDIRECT_URL = '/'    # After successful login → return to the homepage
LOGOUT_REDIRECT_URL = '/'   # After logout → return to the homepage
ACCOUNT_LOGOUT_ON_GET = True # Logout immediately after GET /accounts/logout/ without confirmation

# Social account: do not create an additional email/password if you already have a social account with email
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True