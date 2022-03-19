from .base import *

DEBUG = True

INSTALLED_APPS += ["django_extensions"]  # noqa F405

# Allow all host headers.
ALLOWED_HOSTS = ['*']

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'OPTIONS': {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}