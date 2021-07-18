from .base import *
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = 'os.getenv("SECRET_KEY")'
TEMPLATES[0]['DIRS'] = [os.path.join('templates')]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DBNAME"),
        'USER': os.getenv("DBUSER"),
        'PASSWORD': os.getenv("DBPASS"),
        'HOST': os.getenv("DBHOST"),
        'PORT': 5432
    }
}

REST_FRAMEWORK['DEFAULT_PERMISSION_CLASSES'] = ['rest_framework.permissions.AllowAny']

HOST_ADDRESS = 'localhost:8000'
STATICFILES_DIRS = [os.path.join('static')]
STATIC_ROOT = os.path.join('staticfiles')

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]