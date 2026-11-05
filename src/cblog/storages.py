from storages.backends.s3 import S3Storage


class MediaStore(S3Storage):
    location = "media"
    file_overwrite = False
