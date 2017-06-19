from .base import *


SECRET_KEY = '@$fa*2agx6!&1xkwwyn3o0$on(f2+3z%8abu)s$*2virx-4lyi'

DEBUG = True

ALLOWED_HOSTS = []

STATIC_PATH = os.path.join(PROJECT_DIR, 'static')

STATICFILES_DIRS = (
    STATIC_PATH,
)


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
