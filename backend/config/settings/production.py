"""
Production settings for Build migration project.

- Use Redis for cache
- Use sentry for error logging
"""
import os
import urllib

import sentry_sdk

from sentry_sdk.integrations.django import DjangoIntegration

from .base import *  # noqa

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env("DJANGO_SECRET_KEY")


# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)  # noqa F405
DATABASES["default"]["ENGINE"] = "django_prometheus.db.backends.postgresql"


# APPLICATION VERSION
# ------------------------------------------------------------------------------
APP_VERSION = "unknown"
if os.path.exists(str(APPS_DIR.path(".appversion"))):
    APP_VERSION = APPS_DIR.file(".appversion").read().strip()


# GIT COMMIT
# ------------------------------------------------------------------------------
GIT_COMMIT = "unknown"
if os.path.exists(str(APPS_DIR(".gitcommit"))):
    GIT_COMMIT = APPS_DIR.file(".gitcommit").read().strip()


API_MIDDLEWARE = ["build_migration.contrib.middleware.VersionMiddleware"]
PROMETHEUS_MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]
MIDDLEWARE = (
    [PROMETHEUS_MIDDLEWARE[0]]
    + API_MIDDLEWARE
    + MIDDLEWARE
    + [PROMETHEUS_MIDDLEWARE[1]]
)


# SENTRY SDK CLIENT
# ------------------------------------------------------------------------------
# Senty DNS is taken from SENTRY_DSN environment variable
# https://sentry.io/for/django/
# https://sentry.io/for/celery/
# https://docs.sentry.io/platforms/python/logging/
SENTRY_ENVIRONMENT = env("SENTRY_ENVIRONMENT", default="production")

# https://docs.sentry.io/workflow/releases/?platform=python
SENTRY_RELEASE = f"build_migration@{APP_VERSION}"



sentry_sdk.init(
    release=SENTRY_RELEASE,
    environment=SENTRY_ENVIRONMENT,
    integrations=[  # fmt: off
        DjangoIntegration(),  # fmt: off
    ],  # fmt: off
)


# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-browser-xss-filter
SECURE_BROWSER_XSS_FILTER = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"


# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS", default=["build-migration.plentific.com"]
)
# END SITE CONFIGURATION

INSTALLED_APPS += ["gunicorn", "django_prometheus"]


# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="Build migration <noreply@build-migration.plentific.com>",
)
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default="[Build migration]")
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)


# TEMPLATES
# ------------------------------------------------------------------------------
# Keep templates in memory so tests run faster.
# See:
# https://docs.djangoproject.com/en/dev/ref/templates/api/#django.template.loaders.cached.Loader
TEMPLATES[0]["OPTIONS"]["loaders"] = [
    (
        "django.template.loaders.cached.Loader",
        [
            "django.template.loaders.filesystem.Loader",
            "django.template.loaders.app_directories.Loader",
        ],
    )
]


# CACHING
# ------------------------------------------------------------------------------
REDIS_URL = env.str("REDIS_URL")
REDIS_DB = env.int("REDIS_DB", default=0)
REDIS_LOCATION = urllib.parse.urljoin(REDIS_URL, str(REDIS_DB))

# Heroku URL does not pass the DB number, so we parse it in
CACHES = {
    "default": {
        "BACKEND": "django_prometheus.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": False,
            # mimics memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
        },
    }
}


# https://github.com/django/django/blob/3.1/django/utils/log.py
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
    },
    "loggers": {
        "django": {"handlers": ["console", "mail_admins"], "level": "INFO"},
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# URLs
# ------------------------------------------------------------------------------
# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin")


# DJANGO PROMETHEUS
# ------------------------------------------------------------------------------
PROMETHEUS_EXPORT_MIGRATIONS = (
    False
)  # if set to True Prometheus will monitor total number of applied and
# unapplied migrations by connection


# CORS
# ------------------------------------------------------------------------------
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST")
CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST


# Your production stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
