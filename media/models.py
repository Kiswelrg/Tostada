from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your models here.
class MediaFileSystemStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, *args, **kwargs):
        super().__init__(location, *args, **kwargs)