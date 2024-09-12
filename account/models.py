from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from .util import getUserCode
from django.dispatch import receiver
from project.snowflake import getAccountAUserSnowflakeID
from hashlib import md5
import os
from UtilGlobal.validator.FieldFile import imagefile_validator
from media.models import MediaFileSystemStorage

# Create your models here.
    

class AUser(User):
    @staticmethod
    def md5_filename(n):
        s = os.path.splitext(n)
        return md5(s[0].encode('utf-8')).hexdigest() + s[1]

    def cover_dir_path(instance, filename):
        return f'usercover/{instance.urlCode}/' + AUser.md5_filename(filename)

    def avatar_dir_path(instance, filename):
        return f'avatar/{instance.urlCode}/' + AUser.md5_filename(filename)
    
    name = models.CharField(max_length=20,default='some_user')
    # username = models.CharField(  #只能包含_和数字 开头不能有数字或_ _不能2连 结尾不能_
    #     unique=True,
    #     null=False,
    #     blank=False,
    #     db_index=True,
    #     max_length=24,
    #     validators=[
    #         RegexValidator(
    #             regex=r'^(?=.{6,20}$)(?![_0-9])(?!.*[_]{2})[a-zA-Z0-9_]+(?<![_])$',
    #             message='Enter a valid username',
    #             code='invalid_username'
    #         ),
    #     ]
    # )
    urlCode = models.PositiveBigIntegerField(default=getAccountAUserSnowflakeID, unique=True, db_index=True, primary_key=True)
    # sex = models.CharField(default='2',max_length = 2,choices = {('0', '男'),('1', '女'),('2', '0b01')})
    age = models.PositiveSmallIntegerField(default=None,blank=True,null=True)
    info = models.FileField(default=None,blank=True,null=True)
    additional = models.JSONField(default=None, blank=True, null=True)
    cover = models.ImageField(upload_to=cover_dir_path, blank=True, default='', validators=[imagefile_validator], storage=MediaFileSystemStorage)
    avatar = models.ImageField(upload_to=avatar_dir_path, blank=True, default='default/user/user.svg',validators=[imagefile_validator], storage=MediaFileSystemStorage)

    def __str__(self) -> str:
        return f"{self.username}({self.urlCode})"
    
    class Meta:
        ordering = ['urlCode']


    

@receiver(models.signals.post_delete, sender=AUser)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MyModel` object is deleted.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)
    if instance.cover:
        if os.path.isfile(instance.cover.path):
            os.remove(instance.cover.path)

@receiver(models.signals.pre_save, sender=AUser)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `AUser` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        u = AUser.objects.get(pk=instance.pk)
        old_files = [u.avatar, u.cover]
    except AUser.DoesNotExist:
        return False

    if all([f == '' for f in old_files]):
        return
    new_files = [instance.avatar, instance.cover]
    
    for i in range(len(old_files)):
        old_file = old_files[i]
        new_file = new_files[i]
        if not old_file == new_file:
            if old_file and os.path.isfile(old_file.path):
                os.remove(old_file.path)
