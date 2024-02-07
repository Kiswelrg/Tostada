from django.db import models
from django.utils import timezone
from . import util
# Create your models here.

def EmptyJson():
    return {}

class ToolServer(models.Model):
    def cover_dir_path(instance, filename):
        return f'{instance.__class__.__name__}/{instance.id}/cover/' + instance.date_add.strftime('%Y/%m/%d/' + filename)
    def logo_dir_path(instance, filename):
        return f'{instance.__class__.__name__}/{instance.id}/logo/' + instance.date_add.strftime('%Y/%m/%d/' + filename)

    ts_status = [
        ('0', 'destroyed'),
        ('1', 'public'),
        ('2', 'private'),
        ('3', 'archived'),
    ]
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    urlCode = models.IntegerField(default=util.getToolServerCode, unique=True, db_index=True)
    date_created = models.DateTimeField(default=timezone.now)
    type = models.PositiveSmallIntegerField(default=0)
    owner = models.ForeignKey(
        "user.User",
        on_delete = models.CASCADE
    )
    status = models.CharField(
        max_length=2,
        choices=ts_status,
        default='1'
    )
    cover = models.ImageField(upload_to=cover_dir_path,blank=True, default='')
    logo = models.ImageField(upload_to=logo_dir_path,blank=True, default='')
    additional = models.JSONField(default = EmptyJson, null = True)



class Tool(models.Model):
    def cover_dir_path(instance, filename):
        return f'{instance.__class__.__name__}/{instance.id}/cover/' + instance.date_add.strftime('%Y/%m/%d/' + filename)
    def logo_dir_path(instance, filename):
        return f'{instance.__class__.__name__}/{instance.id}/logo/' + instance.date_add.strftime('%Y/%m/%d/' + filename)

    server = models.ForeignKey(ToolServer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    t_status = [
        ('0', 'destroyed'),
        ('1', 'public'),
        ('2', 'private'),
        ('3', 'archived'),
    ]
    urlCode = models.IntegerField(default=util.getToolCode, unique=True, db_index=True)
    date_created = models.DateTimeField(default=timezone.now)
    type = models.PositiveSmallIntegerField(default=0)
    status = models.CharField(
        max_length=2,
        choices=t_status,
        default='1'
    )
    cover = models.ImageField(upload_to=cover_dir_path,blank=True, default='')
    logo = models.ImageField(upload_to=logo_dir_path,blank=True, default='')
    additional = models.JSONField(default = EmptyJson, null = True)


class ServerAuthorizationLevels(models.Model):
    title = models.CharField(max_length = 128)
    description = models.CharField(max_length = 256, default = '')
    type = models.CharField(max_length = 2,
                            default = '0',
                            choices = [
        ('0', 'binary'),
    ])
    category = models.CharField(max_length = 2,
                                default = '0',
                                choices = [
        ('0', 'General Server Permissions'),
        ('1', 'Other Permissions'),
    ])

class ToolAuthorizationLevels(models.Model):
    title = models.CharField(max_length = 128)
    description = models.CharField(max_length = 256, default = '')
    type = models.CharField(max_length = 2,
                            default = '0',
                            choices = [
        ('0', 'binary'),
    ])
    category = models.CharField(max_length = 2,
                                default = '0',
                                choices = [
        ('0', 'General Tool Permissions'),
        ('1', 'Membership Permissions'),
        ('2', 'Other Permissions'),
    ])
    date_created = models.DateTimeField(default=timezone.now)



class UserServerAuthorization(models.Model):
    auth_type = models.ForeignKey(
        ServerAuthorizationLevels,
        on_delete = models.CASCADE
    )
    auth_value_bool = models.BooleanField(default = False)
    user = models.ForeignKey(
        'user.User',
        on_delete = models.CASCADE
    )
    server = models.ForeignKey(
        ToolServer,
        on_delete = models.CASCADE
    )
    date_added = models.DateTimeField(default=timezone.now)


class UserToolAuthorization(models.Model):
    auth_type = models.ForeignKey(
        ToolAuthorizationLevels,
        on_delete = models.CASCADE
    )
    auth_value_bool = models.BooleanField(default = False)
    user = models.ForeignKey(
        'user.User',
        on_delete = models.CASCADE
    )
    tool = models.ForeignKey(
        Tool,
        on_delete = models.CASCADE
    )
    date_added = models.DateTimeField(default=timezone.now)