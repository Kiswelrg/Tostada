from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone
from .util import getUserCode
from django.dispatch import receiver
import os
# Create your models here.
class AUser(User):
    def cover_dir_path(instance, filename):
        return f'cover/user-{instance.urlCode}/' + instance.date_add.strftime('%Y-%m-%d/' + filename)

    def avatar_dir_path(instance, filename):
        return f'avatar/user-{instance.urlCode}/' + instance.date_add.strftime('%Y-%m-%d/' + filename)
    
    name = models.CharField(max_length=20,default='some_user')
    # username = models.CharField(                                                        #只能包含_和数字 开头不能有数字或_ _不能2连 结尾不能_
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
    urlCode = models.PositiveBigIntegerField(default=getUserCode, unique=True, db_index=True)
    # password = models.CharField(max_length=64)
    sex = models.CharField(
            default='隐藏',
            max_length = 2,
            choices = {
                ('0', '男'),
                ('1', '女'),
            },
        )
    age = models.PositiveSmallIntegerField(default=None,blank=True,null=True)
    # date_add = models.DateTimeField(default=timezone.now)
    info = models.FileField(default=None,blank=True,null=True)
    # email = models.EmailField(max_length = 25, null = True, blank = True)
    additional = models.JSONField(default=None, blank=True, null=True)
    cover = models.ImageField(upload_to=cover_dir_path, blank=True, default='')
    avatar = models.ImageField(upload_to=avatar_dir_path, blank=True, default='')

    def __str__(self) -> str:
        return f"{self.username}({self.urlCode})"

    

@receiver(models.signals.post_delete, sender=AUser)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MyModel` object is deleted.
    """
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)

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
        old_file = AUser.objects.get(pk=instance.pk).avatar
    except AUser.DoesNotExist:
        return False

    if old_file == '':
        return
    new_file = instance.avatar
    
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
