"""
Production settings for Google App Engine deployment.
Optimized for cost efficiency and minimal resource usage.
"""

import os

from .settings import *  # noqa: F403


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")

# Allow App Engine hostnames
ALLOWED_HOSTS = ["*"]  # In production, be more specific with your domain

# Database configuration - SQLite for cost efficiency
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
        # SQLite optimizations for performance
        "OPTIONS": {
            "timeout": 10,
            "check_same_thread": False,
        },
    }
}

# Static files configuration for App Engine
STATIC_URL = "/static/"
STATIC_ROOT = "static"

# Cache settings for performance and cost reduction
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
        "TIMEOUT": 300,  # 5 minutes
    }
}

# Session optimization
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 86400  # 24 hours

# Security settings for production
SECURE_SSL_REDIRECT = False  # App Engine handles SSL termination
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# Logging configuration - minimal for cost efficiency
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "WARNING",  # Only log warnings and errors
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# Performance optimizations
USE_TZ = True
USE_I18N = False  # Disable if not using internationalization
USE_L10N = False  # Disable if not using localization

# Email backend for cost efficiency (console for now)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
