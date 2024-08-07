from django.db import models
from message.models import Message

# Create your models here.

class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')

    def __str__(self):
        return self.file.name