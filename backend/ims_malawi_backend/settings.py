# ims_malawi_backend/settings.py
import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
import django.conf.locale
import dj_database_url

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================
# ENVIRONMENT DETECTION
# ==============================================

# Detect if running on Render
ON_RENDER = os.environ.get('RENDER', False)
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ==============================================
# SECURITY SETTINGS
# ==============================================

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-your-secret-key-here-change-in-production')

# ALLOWED HOSTS - Render deployment
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com', 'ims-malawi-backend.onrender.com']

# Add Render's external hostname automatically
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# ==============================================
# APPLICATION DEFINITION
# ==============================================

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    'core.apps.CoreConfig',
    'content.apps.ContentConfig',
    'payments.apps.PaymentsConfig',
    'subscriptions.apps.SubscriptionsConfig',
    'comments.apps.CommentsConfig',
    'analytics.apps.AnalyticsConfig',
]

# ==============================================
# MIDDLEWARE
# ==============================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ims_malawi_backend.urls'

# ==============================================
# TEMPLATES
# ==============================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ims_malawi_backend.wsgi.application'

# ==============================================
# DATABASE CONFIGURATION
# ==============================================

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ==============================================
# PASSWORD VALIDATION
# ==============================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================
# INTERNATIONALIZATION & LANGUAGE SETTINGS
# ==============================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Blantyre'
USE_I18N = True
USE_TZ = True

EXTRA_LANG_INFO = {
    'ny': {
        'bidi': False,
        'code': 'ny',
        'name': 'Chichewa',
        'name_local': 'Chichewa',
    },
}

django.conf.locale.LANG_INFO.update(EXTRA_LANG_INFO)

LANGUAGES = [
    ('en', 'English'),
    ('ny', 'Chichewa'),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# ==============================================
# STATIC & MEDIA FILES
# ==============================================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================
# DEFAULT PRIMARY KEY
# ==============================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================
# REST FRAMEWORK
# ==============================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# ==============================================
# CORS CONFIGURATION
# ==============================================

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://ims-malawi-backend.onrender.com",
]

CORS_ALLOW_CREDENTIALS = True

# ==============================================
# JAZZMIN CONFIGURATION - FIXED FOR PRODUCTION
# ==============================================

JAZZMIN_SETTINGS = {
    "site_title": "IMS Malawi Union Admin",
    "site_header": "IMS Malawi Union",
    "site_brand": "IMS Malawi",
    "site_icon": "/static/admin/img/ims-icon.png", 
    "welcome_sign": "Welcome to IMS Malawi Union Admin Panel",
    "copyright": "IMS Malawi Union",
    "search_model": ["auth.User", "content.ContentItem"],
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "View Site", "url": "/", "new_window": True},
    ],
    "show_ui_builder": True,
    "language_chooser": True,
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["auth", "content", "core", "payments"],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "content.ContentItem": "fas fa-photo-video",
        "content.Event": "fas fa-calendar-alt",
        "content.Gallery": "fas fa-images",
        "content.Ministry": "fas fa-church",
        "subscriptions.Subscriber": "fas fa-envelope",
        "comments.Comment": "fas fa-comments",
        "analytics.ActivityLog": "fas fa-chart-line",
        "payments.Donation": "fas fa-hand-holding-usd",
        "core.ChurchLeadership": "fas fa-user-tie",
        "core.PrayerRequest": "fas fa-pray",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
}

# ==============================================
# AUTHENTICATION & LOGIN/REDIRECT SETTINGS
# ==============================================

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_URL = '/admin/logout/'
LOGOUT_REDIRECT_URL = '/admin/login/'

# ==============================================
# PRODUCTION SECURITY SETTINGS
# ==============================================

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ==============================================
# LOGGING CONFIGURATION
# ==============================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# ==============================================
# MONKEY PATCH FOR length_is FILTER
# ==============================================

from django import template
from django.template import defaultfilters

@defaultfilters.register.filter(name='length_is')
def length_is(value, arg):
    """Restore the deprecated length_is filter"""
    try:
        return len(value) == int(arg)
    except (ValueError, TypeError):
        return False

if not hasattr(defaultfilters, 'length_is'):
    defaultfilters.length_is = length_is