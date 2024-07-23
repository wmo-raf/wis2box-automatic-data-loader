"""
Django settings for wis2box_adl project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from pathlib import Path

import dj_database_url
import environ
import importlib
from wis2box_adl.version import VERSION

from django.core.exceptions import ImproperlyConfigured

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
)

dev_env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR))), ".env")

if os.path.isfile(dev_env_path):
    # reading .env file
    environ.Env.read_env(dev_env_path)

# Application definition
INSTALLED_APPS = [
    "wis2box_adl.home",
    "wis2box_adl.core",

    "django_countries",
    "django_celery_beat",

    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.contrib.settings",
    "wagtail.contrib.styleguide",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    "django_cleanup.apps.CleanupConfig",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.gis",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

WIS2BOX_ADL_PLUGIN_DIR_PATH = Path(env.str("WIS2BOX_ADL_PLUGIN_DIR_PATH", "/wis2boxadl/plugins"))

if WIS2BOX_ADL_PLUGIN_DIR_PATH.exists():
    WIS2BOX_ADL_PLUGIN_FOLDERS = [file for file in WIS2BOX_ADL_PLUGIN_DIR_PATH.iterdir() if file.is_dir()]
else:
    WIS2BOX_ADL_PLUGIN_FOLDERS = []

WIS2BOX_ADL_PLUGIN_NAMES = [d.name for d in WIS2BOX_ADL_PLUGIN_FOLDERS]

if WIS2BOX_ADL_PLUGIN_NAMES:
    print(f"Loaded WIS2Box ADL plugins: {','.join(WIS2BOX_ADL_PLUGIN_NAMES)}")
    INSTALLED_APPS.extend(WIS2BOX_ADL_PLUGIN_NAMES)

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "wis2box_adl.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "wis2box_adl.config.wsgi.application"
ASGI_APPLICATION = "wis2box_adl.config.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = env.str("TIMEZONE", "UTC")

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, "static"),
]

STATIC_ROOT = env.str("STATIC_ROOT", os.path.join(BASE_DIR, "static"))
STATIC_URL = "/static/"

MEDIA_ROOT = env.str("MEDIA_ROOT", os.path.join(BASE_DIR, "media"))
MEDIA_URL = "/media/"

# Default storage settings, with the staticfiles storage updated.
# See https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-STORAGES
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # ManifestStaticFilesStorage is recommended in production, to prevent
    # outdated JavaScript / CSS assets being served from cache
    # (e.g. after a Wagtail upgrade).
    # See https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/#manifeststaticfilesstorage
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
    },
}

# Wagtail settings

WAGTAIL_SITE_NAME = "WIS2Box ADL"

# Search
# https://docs.wagtail.org/en/stable/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {
        "BACKEND": "wagtail.search.backends.database",
    }
}

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
WAGTAILADMIN_BASE_URL = "http://example.com"

# Allowed file extensions for documents in the document library.
# This can be omitted to allow all files, but note that this may present a security risk
# if untrusted users are allowed to upload files -
# see https://docs.wagtail.org/en/stable/advanced_topics/deploying.html#user-uploaded-files
WAGTAILDOCS_EXTENSIONS = ['csv', 'docx', 'key', 'odt', 'pdf', 'pptx', 'rtf', 'txt', 'xlsx', 'zip']

REDIS_HOST = env.str("REDIS_HOST", "redis")
REDIS_PORT = env.str("REDIS_PORT", "6379")
REDIS_USERNAME = env.str("REDIS_USER", "")
REDIS_PASSWORD = env.str("REDIS_PASSWORD", "")
REDIS_PROTOCOL = env.str("REDIS_PROTOCOL", "redis")
REDIS_URL = env.str(
    "REDIS_URL",
    f"{REDIS_PROTOCOL}://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0",
)

CELERY_BROKER_URL = REDIS_URL
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_SINGLETON_BACKEND_CLASS = (
    "wis2box_adl.celery_singleton_backend.RedisBackendForSingleton"
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "wis2box-adl-default-cache",
        "VERSION": VERSION,
    },
}

# WIS2Box Configuration
WIS2BOX_CENTRE_ID = env.str("WIS2BOX_CENTRE_ID", None)
WIS2BOX_STORAGE_ENDPOINT = env.str("WIS2BOX_STORAGE_ENDPOINT", None)
WIS2BOX_STORAGE_USERNAME = env.str("WIS2BOX_STORAGE_USERNAME", None)
WIS2BOX_STORAGE_PASSWORD = env.str("WIS2BOX_STORAGE_PASSWORD", None)

if WIS2BOX_CENTRE_ID is None:
    raise ImproperlyConfigured("WIS2BOX_CENTRE_ID is not set")

if WIS2BOX_STORAGE_ENDPOINT is None:
    raise ImproperlyConfigured("WIS2BOX_STORAGE_ENDPOINT is not set")

if WIS2BOX_STORAGE_USERNAME is None:
    raise ImproperlyConfigured("WIS2BOX_STORAGE_USERNAME is not set")

if WIS2BOX_STORAGE_PASSWORD is None:
    raise ImproperlyConfigured("WIS2BOX_STORAGE_PASSWORD is not set")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        # Send logs with at least INFO level to the console.
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s"
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# Allows accessing and setting values on a dictionary like an object. Using this
# we can pass plugin authors and other functions a `settings` object which can modify
# the settings like they expect (settings.SETTING = 'test') etc.


class AttrDict(dict):
    def __getattr__(self, item):
        return super().__getitem__(item)

    def __setattr__(self, item, value):
        globals()[item] = value

    def __setitem__(self, key, value):
        globals()[key] = value


for plugin in [*WIS2BOX_ADL_PLUGIN_NAMES]:
    try:
        mod = importlib.import_module(plugin + ".config.settings.settings")
        # The plugin should have a setup function which accepts a 'settings' object.
        # This settings object is an AttrDict shadowing our local variables so the
        # plugin can access the Django settings and modify them prior to startup.
        result = mod.setup(AttrDict(vars()))
    except ImportError as e:
        print("Could not import %s", plugin)
        print(e)
