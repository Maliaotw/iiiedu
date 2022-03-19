from .base import *  # noqa

import io
import os
import google.auth
from google.cloud import secretmanager
from google.oauth2 import service_account

# # Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass

# [END_EXCLUDE]
if os.environ.get("GOOGLE_CLOUD_PROJECT") and os.environ.get("SETTINGS_NAME"):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    client = secretmanager.SecretManagerServiceClient()
    settings_name = env("SETTINGS_NAME")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")
    env.read_env(io.StringIO(payload))

DJANGO_SUPERUSER_USERNAME = env("DJANGO_SUPERUSER_USERNAME")
DJANGO_SUPERUSER_PASSWORD = env("DJANGO_SUPERUSER_PASSWORD")

GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
    BASE_DIR / 'credentials.json'
)

DEFAULT_FILE_STORAGE = 'src.gcloud.GoogleCloudMediaFileStorage'
STATICFILES_STORAGE = 'src.gcloud.GoogleCloudStaticFileStorage'
GS_MEDIA_BUCKET_NAME = env("GS_MEDIA_BUCKET_NAME")
GS_STATIC_BUCKET_NAME = env("GS_STATIC_BUCKET_NAME")
GS_PROJECT_ID = env("GS_PROJECT_ID")
MEDIA_URL = f'https://storage.googleapis.com/{GS_MEDIA_BUCKET_NAME}/'
# GS_DEFAULT_ACL = 'publicRead'
# GS_QUERYSTRING_AUTH = False
# GS_DEFAULT_ACL = None

# GENERAL
# ------------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DEBUG", False)

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# MIDDLEWARE
# MIDDLEWARE.append('django.middleware.security.SecurityMiddleware')
# MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')


# Database
# [START cloudrun_django_database_config]
# Use django-environ to parse the connection string
# DATABASES = {"default": env.db()}
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

# If the flag as been set, configure to use proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = "1234"
    DATABASES["default"]["NAME"] = os.environ.get('DATABASE_NAME', 'unodesign')

#
# [END cloudrun_django_database_config]
