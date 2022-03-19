from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting


class GoogleCloudMediaFileStorage(GoogleCloudStorage):
    bucket_name = setting('GS_MEDIA_BUCKET_NAME')


class GoogleCloudStaticFileStorage(GoogleCloudStorage):
    bucket_name = setting('GS_STATIC_BUCKET_NAME')
