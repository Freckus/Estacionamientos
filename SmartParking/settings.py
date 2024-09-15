import os
import pymysql
pymysql.install_as_MySQLdb()
from pathlib import Path
#from django.contrib.auth.models import AbstractUser

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR=os.path.join(BASE_DIR,'templates')

#carpeta de media images de los qr

SECRET_KEY = 'django-insecure-80w6m67$=kxsj#ui4yxffv1nkt#lcny78a!yl3!3z-rz7h9@!!'

DEBUG = True

ALLOWED_HOSTS = ['*']

##
#https://stackoverflow.com/questions/75121950/how-to-use-authenticate-method-with-abstractuser-model-django
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Reserva' 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #cerrar sesion 
    #'django.contrib.sessions.middleware.SessionMiddleware',
    #'django_session_timeout.middleware.SessionTimeoutMiddleware',
]
    

ROOT_URLCONF = 'SmartParking.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'SmartParking.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smartparking2',
        'USER':'root',
        'PASSWORD':'admin',
        'PORT': '3306',
    }
}


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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#EMAIL CONFIG
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'smartparking310@gmail.com'  
EMAIL_HOST_PASSWORD ='oxim zcet atyn wybe'  
EMAIL_USE_TLS = True

#django.contrib.auth.backends.ModelBackend 
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')