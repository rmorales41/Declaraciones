"""
Django settings for declaracion project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y%9#l8%x*0^%l5o(*z44+83m4ehbe+3^&m$yfvn!e1s7l&b9nl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# mensajes 
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'libreria',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'declaracion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # templates in blog app                        
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

WSGI_APPLICATION = 'declaracion.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME':'Declaraciones',
        'HOST':'127.0.0.1',
        'PORT':'1433',
        'USER':'sa',
        'PASSWORD':'0026',
        'ATOMIC_REQUESTS': True,
        
        'OPTIONS':{
            'driver':'ODBC Driver 17 for SQL Server',
            'init.command':"SET sql_mode='STRICT_TRANS_TABLES'" ,
                  },
    },
} 

# base conexion 2
#DATABASES = {
#    'default': {
#        'ENGINE': 'mssql',
#        'NAME':'Declaraciones',
#        'HOST':'127.0.0.1',
#        'PORT':'1433',
#        'USER':'sa',
#        'PASSWORD':'0026',
#        'ATOMIC_REQUESTS': True,
#        
#        'OPTIONS':{
#            'driver':'ODBC Driver 17 for SQL Server',
#            'init.command':"SET sql_mode='STRICT_TRANS_TABLES'" ,
#                  },
#    },
#} 


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# para poder manejar las imagenes

MEDIA_ROOT = os.path.join(BASE_DIR,'')
MEDIA_URL = '/'

# Configuración para enviar correos electrónicos
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Backend para enviar correos SMTP


# Configuración del servidor SMTP
EMAIL_HOST = 'SMTP.SIPAVINT.COM'                    # Host del servidor SMTP
EMAIL_PORT = 25                                     # Puerto del servidor SMTP (normalmente 587 para TLS/STARTTLS)
EMAIL_USE_TLS = False                                 # Usar TLS para cifrado de conexión
EMAIL_HOST_USER = 'facturas227@sipavint.com'        # Dirección de correo electrónico desde la cual enviar los correos
EMAIL_HOST_PASSWORD = 'SipavBelen'                  # Contraseña de la cuenta de correo electrónico
DEFAULT_FROM_EMAIL = 'coordinador.ti@sipavint.com'  # Dirección de correo por defecto para los correos enviados



# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
