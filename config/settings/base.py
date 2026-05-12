"""
Django settings for config project.
"""

from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta
import os

# ===================== LOAD ENV =====================

load_dotenv()

# ===================== BASE DIR =====================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ===================== SECURITY =====================

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = ['*']

# ===================== APPLICATIONS =====================

INSTALLED_APPS = [

    # DJANGO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # THIRD PARTY
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular', 

    # LOCAL APPS
    'accounts',
    'academics',
    'subjects',
    'applications',
    'memoires',
    'defenses',
    'common',
]

# ===================== MIDDLEWARE =====================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← en premier obligatoirement
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ===================== CORS =====================

CORS_ALLOW_ALL_ORIGINS = True  # En développement seulement

# ===================== ROOT URL =====================

ROOT_URLCONF = 'config.urls'

# ===================== TEMPLATES =====================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# ===================== WSGI =====================

WSGI_APPLICATION = 'config.wsgi.application'

# ===================== DATABASE =====================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# ===================== CUSTOM USER =====================

AUTH_USER_MODEL = 'accounts.User'

# ===================== PASSWORD VALIDATORS =====================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

# ===================== INTERNATIONALIZATION =====================

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Africa/Ouagadougou'

USE_I18N = True

USE_TZ = True

# ===================== DJANGO REST FRAMEWORK =====================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# ===================== JWT =====================

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ===================== STATIC FILES =====================

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

# ===================== MEDIA FILES =====================

MEDIA_URL = '/media/'

MEDIA_ROOT = BASE_DIR / 'media'

# ===================== DEFAULT PRIMARY KEY =====================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'