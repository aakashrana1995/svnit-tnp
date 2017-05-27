from tnp.settings.base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = [] #Put server's IP address here


#Set up database settings here
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': 3306,
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

#Following settings accordings to manage.py check --deploy

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True #Check this once

CSRF_COOKIE_SECURE = True

CSRF_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = 'DENY'