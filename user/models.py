from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=20,default='some_user')
    username = models.CharField(                                                        #只能包含_和数字 开头不能有数字或_ _不能2连 结尾不能_
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        max_length=24,
        validators=[
            RegexValidator(
                regex=r'^(?=.{6,20}$)(?![_0-9])(?!.*[_]{2})[a-zA-Z0-9_]+(?<![_])$',
                message='Enter a valid username',
                code='invalid_username'
            ),
        ]
    )
    password = models.CharField(max_length=64)
    sex = models.PositiveSmallIntegerField(default=None,blank=True,null=True)
    age = models.PositiveSmallIntegerField(default=None,blank=True,null=True)
    date_add = models.DateTimeField(default=timezone.now)
    info = models.FileField(default=None,blank=True,null=True)
    additional = models.JSONField(default=None, blank=True, null=True)