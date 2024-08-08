from django.db import models
from message.models import Message
from django.conf import settings
from django.utils import timezone
from project.snowflake import AttachmentGMFileSnowflakeID
from django.dispatch import receiver
import datetime
import hashlib
import os
from django.core.files.storage import FileSystemStorage


# Create your models here.



class AttachmentFileSystemStorage(FileSystemStorage):
    def __init__(self, location=settings.ATTACHMENT_ROOT, *args, **kwargs):
        super().__init__(location, *args, **kwargs)




class GMFile(models.Model):
    @staticmethod
    def validateURL(url):
        if url[0] == '/':
            url = url[1:]
        if url[-1] == '/':
            url = url[:-1]
        c, a, tail = url.split('/',2)
        fn, args_str = tail.split('?',1)
        required_keys = ['ex','is','hm']
        args = {}
        for p in args_str.split('&'):
            if p:
                k,v = p.split('=',1)
                if k not in required_keys:
                    continue
                args[k] = v
        if any([a not in k for a in required_keys]):
            return False
        if hashlib.sha256((c+a+fn+args['ex']+args['is']+settings.ATTACHMENT_KEY).encode('utf-8')).hexdigest() == args['hm']:
            if int(args['ex'],16) > timezone.now().timestamp():
                return True
        return False

    def refreshURL(self, f):
        url = f.url
        if GMFile.validateURL(url):
            return url
        d = {}
        now = timezone.now()
        ex = now + datetime.timedelta(days=1)
        d['is'] = hex(round(now.timestamp()))[2:]
        d['ex'] = hex(round(ex.timestamp()))[2:]
        channel_cid = f.message.channel.urlCode
        d['hm'] = hashlib.sha256(
            (channel_cid+f.urlCode+f.file.name+d['ex']+d['is']).encode('utf-8')
        ).hexdigest()
        f.last_url = f"{channel_cid}/{f.urlCode}/{f.file.name}?ex={d['ex']}&is={d['is']}&hm={d['hm']}"
        f.save()
        return f.last_url

    @staticmethod
    def get_file(cid):
        try:
            f = GMFile.objects.get(pk=cid)
        except GMFile.DoesNotExist:
            return None
        return {
            'file': f.file,
            'url': f.refreshURL()
        }
        
    def fileSavePath(instance, fn):
        return f"{instance.message.channel.urlCode}/{instance.urlCode}/{fn}"


    urlCode = models.PositiveBigIntegerField(default=AttachmentGMFileSnowflakeID, unique=True, db_index=True, primary_key=True)
    file = models.FileField(upload_to=fileSavePath, storage=AttachmentFileSystemStorage)
    _type = models.CharField(max_length=24, null=True)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
    last_url = models.URLField(max_length=400, null=True, blank=True)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.file.name}/{self.sent_at.isoformat()}'


@receiver(models.signals.post_delete, sender=GMFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MyModel` object is deleted.
    """
    if instance.file:
        fp = instance.file.path
        if os.path.isfile(fp):
            os.remove(fp)
            d = os.path.dirname(fp)
            if not os.listdir(d):
                os.rmdir(d)

@receiver(models.signals.pre_save, sender=GMFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `GMFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        u = GMFile.objects.get(pk=instance.pk)
        old_files = [u.file]
    except GMFile.DoesNotExist:
        return False

    if all([f == '' for f in old_files]):
        return
    new_files = [instance.file]
    
    for i in range(len(old_files)):
        old_file = old_files[i]
        new_file = new_files[i]
        if not old_file == new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)


