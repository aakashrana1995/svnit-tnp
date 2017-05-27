from tnp.settings.base import *

SECRET_KEY = '@$fa*2agx6!&1xkwwyn3o0$on(f2+3z%8abu)s$*2virx-4lyi'

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tnp',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}

STATIC_URL = '/static/'

MEDIA_URL = '/media/'