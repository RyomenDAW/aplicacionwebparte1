"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

# Directorio para archivos subidos
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Build paths inside the project like this: BASE_DIR / 'subdir'.


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()
SECRET_KEY =  env("SECRET_KEY")


# .env

ADMIN_KEY = os.getenv('ADMIN_KEY')
TECH_SUPPORT_KEY = os.getenv('TECH_SUPPORT_KEY')
SELLER_KEY = os.getenv('SELLER_KEY')
CUSTOMER_KEY = os.getenv('CUSTOMER_KEY')
APPEND_SLASH = True


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["0.0.0.0", "localhost", "127.0.0.1"])
# Explicación del cambio
# env.list() convierte una cadena separada por comas en una lista.
# La configuración en tu archivo .env será convertida automáticamente, por ejemplo:
# env
# Copy
# Edit
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



#ALLOWED_HOSTS = ['127.0.0.1', '.pythonanywhere.com','0.0.0.0']





# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tiendaordenadores',
    'django_seed',
    'django_bootstrap5',
    'django_bootstrap_icons',
    'rest_framework',
    'oauth2_provider', #Esta se añade
   #'rest_framework_simplejwt', #Securizacion
    #'oidc_provider',  # OpenID Connect Provider      / # ESTA LINEA SE AÑADE PARA OICP
]

# # Configuración básica de OIDC
# OIDC_ISSUER = "http://localhost:8000"  # Puerto 8000
# OIDC_IDTOKEN_EXPIRE = 3600 # 1 HORA PARA EXPIRACION
# OIDC_USERINFO = "oidc_provider.lib.claims.StandardScopeClaims"





MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    ]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Aquí puedes agregar rutas a directorios adicionales si es necesario
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


WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'tiendaordenadores.Usuario'

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = BASE_DIR /'static'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_REDIRECT_URL = 'inicio'
LOGOUT_REDIRECT_URL = 'inicio'

OAUTH2_PROVIDER = {
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Acceso a los grupos'},
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600000000,
    'AUTHORIZATION_CODE_EXPIRE_SECONDS': 3600000000,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # 🔥 Asegúrate de que esto está
    ),

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

