from django.db import models
from message.models import ChatMessage
from django.conf import settings
from django.utils import timezone
from project.snowflake import AttachmentMFileSnowflakeID
from django.dispatch import receiver
import datetime
import hashlib
import os
from django.core.files.storage import FileSystemStorage
from PIL import Image
import imghdr

def is_image1(field_file):
    if not field_file:
        return False
    file_type = imghdr.what(field_file)
    return file_type in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']


def is_image(field_file):
    if not field_file:
        return False,0
    try:
        img = Image.open(field_file)
        img.verify()  # Verify the file is an image
        return True,img.size
    except (IOError, SyntaxError):
        return False,0

# Create your models here.



class AttachmentFileSystemStorage(FileSystemStorage):
    def __init__(self, location=settings.ATTACHMENT_ROOT, *args, **kwargs):
        super().__init__(location, *args, **kwargs)




class MFile(models.Model):
    @staticmethod
    def validateURL(url, args = None):
        if args and len(args) > 0:
            url+='?'
            for k in args:
                url+=f"{k}={args[k]}&"
        try:
            if url[0] == '/':
                url = url[1:]
            if url[-1] == '/':
                url = url[:-1]
            c, a, tail = url.split('/',2)
            fn, args_str = tail.split('?',1)
            required_keys = ['ex','is','hm']
            args = {}
            for p in args_str.split('&'):
                if p == '':
                    continue
                if p:
                    k,v = p.split('=',1)
                    if k not in required_keys:
                        continue
                    args[k] = v
            if any([a not in args for a in required_keys]):
                return False
            if hashlib.sha256((f"{c}{a}{fn}{args['ex']}{args['is']}{settings.ATTACHMENT_KEY}").encode('utf-8')).hexdigest() == args['hm']:
                if int(args['ex'],16) > timezone.now().timestamp():
                    return True
            return False
        except ValueError:
            return False

    def refreshURL(self):
        url = self.last_url
        if url is not None and url != '' and MFile.validateURL(url):
            return settings.ATTACHMENT_URL + url
        d = {}
        now = timezone.now()
        ex = now + datetime.timedelta(days=1)
        d['is'] = hex(round(now.timestamp()))[2:]
        d['ex'] = hex(round(ex.timestamp()))[2:]
        channel_cid = self.message.channel.urlCode
        d['hm'] = hashlib.sha256(
            f"{channel_cid}{self.urlCode}{os.path.basename(self.file.name)}{d['ex']}{d['is']}{settings.ATTACHMENT_KEY}".encode('utf-8')
        ).hexdigest()
        self.last_url = f"{channel_cid}/{self.urlCode}/{os.path.basename(self.file.name)}?ex={d['ex']}&is={d['is']}&hm={d['hm']}"
        self.save()
        return settings.ATTACHMENT_URL + self.last_url

    @staticmethod
    def get_file(cid, attrs = None):
        if attrs is None:
            attrs = [
                'type',
                'size',
                'name',
                'url',
                'file',
            ]
        try:
            f = MFile.objects.get(pk=cid)
        except MFile.DoesNotExist:
            return None
        res =  {}
        if 'name' in attrs:
            res['name'] = f.file.name.rsplit('/',1)[1]
        if 'url' in attrs:
            res['url'] = f.refreshURL()
        if 'file' in attrs:
            res['file'] = f.file
        if 'size' in attrs:
            res['size'] = f.file.size
        c = is_image(f.file)
        if c[0]:
            res['dimensions'] = c[1]
        return res
        
    def fileSavePath(instance, fn):
        return f"{instance.message.channel.urlCode}/{instance.urlCode}/{fn}"


    urlCode = models.PositiveBigIntegerField(default=AttachmentMFileSnowflakeID, unique=True, db_index=True, primary_key=True)
    file = models.FileField(upload_to=fileSavePath, storage=AttachmentFileSystemStorage)
    _type = models.CharField(max_length=24, null=True)
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='attachments')
    last_url = models.URLField(max_length=400, null=True, blank=True)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.file.name}/{self.sent_at.isoformat()}'
    
    class Meta:
        ordering = ['urlCode']


@receiver(models.signals.post_delete, sender=MFile)
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

@receiver(models.signals.pre_save, sender=MFile)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        u = MFile.objects.get(pk=instance.pk)
        old_files = [u.file]
    except MFile.DoesNotExist:
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


