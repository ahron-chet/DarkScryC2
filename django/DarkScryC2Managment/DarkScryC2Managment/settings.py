"""
Django settings for DarkScryC2Managment project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path
from secrets import token_urlsafe
import mimetypes
mimetypes.add_type("text/css", ".css", True)



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

FRONT_DIR = BASE_DIR.parent / "DarkScryFront"  
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7srtjwTeXj69tIbITp_AOC3q-5X5Ou9sQdTud9K6qvOXYDhyfne6ysGipkn4ZjZyooXA0WO1Hgx468GQfthPi2vsMLQuyAupt1FWUcc8V0kSfxpZwae_tI'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["django", "127.0.0.1", "localhost"]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}

# Application definition

INSTALLED_APPS = [
    'application',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "corsheaders",
    "channels",
    "ninja"
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'DarkScryC2Managment.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            FRONT_DIR  / 'templates'
        ],
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

# WSGI_APPLICATION = 'DarkScryC2Managment.wsgi.application'
ASGI_APPLICATION = 'DarkScryC2Managment.asgi.application'



# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', default='default_db_name'),
        'USER': os.getenv('DB_USER', default='default_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', default='default_password'),
        'HOST': os.getenv('DB_HOST', default='localhost'),
        'PORT': os.getenv('DB_PORT', default='5432')
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'application.User'


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Where Django collects static files from for production:
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Additional places Django looks for static files:
STATICFILES_DIRS = [
    FRONT_DIR  / 'static',
]

STATIC_URL = '/static/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



JWT_SECRET = os.getenv("DJANGO_JWT_SECRET", token_urlsafe(60))
JWT_REFRESH_SECRET = os.getenv("DJANGO_JWT_REFRESH_SECRET", token_urlsafe(60))
JWT_ALGORITHM = os.getenv("DJANGO_JWT_ALGORITHM", "HS256")
JWT_EXPIRE_SECONDS = int(os.getenv("DJANGO_JWT_EXPIRE_SECONDS", "360000"))
JWT_REFRESH_EXPIRE_SECONDS = int(os.getenv("DJANGO_JWT_REFRESH_EXPIRE_SECONDS", "3240000"))


CORS_ALLOWED_ORIGINS = ["http://localhost:3000", 'http://172.236.98.55:8000']
CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = False