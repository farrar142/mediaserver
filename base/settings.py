"""
Django settings for base project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
import platform
import re
from django.apps import apps
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f_n^plhx+qzzx@@wblfg1$%o#+i+n#)12!$i_(n&aqbufyg0x2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'medias',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'base/templates', ],
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

WSGI_APPLICATION = 'base.wsgi.application'


FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]


MAX_UPLOAD_SIZE = 5242880
DATA_UPLOAD_MAX_MEMORY_SIZE = None
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880
DATA_UPLOAD_MAX_NUMBER_FIELDS = None
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SERVER = "172.17.0.1"
HOME = SERVER
USER = os.getenv("DB_HOST")
PASSWORD = os.getenv("DB_PASSWORD")

print(f"user in settings{USER}")


def ipchooser():
    if platform.system().strip() == "Windows":
        return HOME
    else:
        return SERVER


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'media',
        'USER': USER,
        'PASSWORD': PASSWORD,
        'HOST': ipchooser(),
        'PORT': '3306',
    },
}
REDIS_HOST = f"redis://:{PASSWORD}@{ipchooser()}:6379/1"

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR/'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ASGI_APPLICATION = 'base.asgi.application'

GRAPH_MODELS = {
    'app_labels': [n for n in INSTALLED_APPS if not 'django' in n]
}
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_HOST,
    },
}
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST)],
        },
    },
    'notify': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(REDIS_HOST)],
        },
    },
}
CSRF_TRUSTED_ORIGINS = ['https://blog.honeycombpizza.link']

CELERY_BROKER_URL = REDIS_HOST
CELERY_RESULT_BACKEND = REDIS_HOST
CELERY_CACHE_BACKEND = REDIS_HOST
CELERY_WORKER_CONCURRENCY = 1
CELERY_TIMEZONE = 'Asia/Seoul'
CELERY_ENABLE_UTC = False
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 10
DJANGO_CELERY_BEAT_TZ_AWARE = False


CUSTOM_PREFIX = "TOKEN"
TOKEN_BACKEND_ONLY = False
TOKEN_FILTERED_METHODS = ['POST']
TOKEN_CONTENT_TYPE = "JSON"
TOKEN_TIMES = 1
TOKEN_UNIT_OF_TIME = "hours"
TOKEN_ALLOWED_URL = [
    re.compile(r'^/admin/'),
    re.compile(r'^/admin/(.*)'),
    re.compile(r'^(.*)/api'),
    re.compile(r'^api/signin/'),
]
TOKEN_USE_DJANGO_AUTH = True

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = [
    'https://shopping.honeycombpizza.link', 'https://blog.honeycombpizza.link']
#                          'http://127.0.0.1:8888', 'http://localhost:8888', '*']
CORS_ALLOW_CREDENTIALS = True
