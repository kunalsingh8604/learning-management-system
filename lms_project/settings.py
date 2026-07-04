"""
Django settings for lms_project project.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env locally (optional — for testing with remote Postgres before deploying)
if not os.environ.get('VERCEL'):
    try:
        from dotenv import load_dotenv
        load_dotenv(BASE_DIR / '.env')
    except ImportError:
        pass

IS_VERCEL = bool(os.environ.get('VERCEL'))


def _database_url():
    """Support Supabase, Vercel Postgres, Railway, Render, and other PostgreSQL hosts."""
    for key in (
        'DATABASE_URL',
        'SUPABASE_DATABASE_URL',
        'POSTGRES_URL',
        'POSTGRES_URL_NON_POOLING',
    ):
        value = os.environ.get(key, '').strip()
        if value:
            # Django/psycopg expect postgresql:// not postgres://
            if value.startswith('postgres://'):
                value = 'postgresql://' + value[len('postgres://'):]
            return value
    return None


def _csrf_trusted_origins():
    """Include this deployment's Vercel URLs automatically."""
    origins = set()

    for env_key in (
        'VERCEL_PROJECT_PRODUCTION_URL',
        'VERCEL_URL',
        'VERCEL_BRANCH_URL',
    ):
        host = os.environ.get(env_key, '').strip()
        if host:
            origins.add(f'https://{host}')

    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(','):
        origin = origin.strip()
        if origin:
            origins.add(origin)

    origins.update({
        'https://learning-management-system-theta-blush.vercel.app',
        'https://learning-management-system-efy4.vercel.app',
    })
    return sorted(origins)


DATABASE_URL = _database_url()
PERSISTENT_DATABASE = bool(DATABASE_URL)

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-lms-project-secret-key-change-in-production-2024',
)

DEBUG = os.environ.get('DEBUG', 'False' if IS_VERCEL else 'True').lower() in (
    '1',
    'true',
    'yes',
)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get('ALLOWED_HOSTS', '*').split(',')
    if host.strip()
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'courses',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'lms_project.urls'

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
                'lms_project.context_processors.deployment',
            ],
        },
    },
]

WSGI_APPLICATION = 'lms_project.wsgi.application'

# Database — PostgreSQL on Vercel (required for real accounts)
if DATABASE_URL:
    import dj_database_url

    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=0,
            conn_health_checks=True,
            ssl_require='sslmode=disable' not in DATABASE_URL,
        )
    }
elif IS_VERCEL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
WHITENOISE_USE_FINDERS = True

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/dashboard/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

if IS_VERCEL and PERSISTENT_DATABASE:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = _csrf_trusted_origins()
