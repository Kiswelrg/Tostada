from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

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

    def __str__(self) -> str:
        return self.name


class Tool(models.Model):
    
    def cover_dir_path(instance, filename):
        return f'{instance.__class__.__name__}/{instance.id}/cover/' + instance.date_add.strftime('%Y/%m/%d/' + filename)
    def logo_dir_path(instance, filename):
        return f'{instance.__class__.__name__}/{instance.id}/logo/' + instance.date_add.strftime('%Y/%m/%d/' + filename)
    def isValidType(value):
        types = [
            ('0', 'I/O'),
            ('1', 'others'),
        ]
        return value in [int(t[0]) for t in types]

    t_status = [
        ('0', 'destroyed'),
        ('1', 'public'),
        ('2', 'private'),
        ('3', 'archived'),
    ]

    server = models.ForeignKey(ToolServer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    urlCode = models.IntegerField(default=util.getToolCode, unique=True, db_index=True)
    date_created = models.DateTimeField(default=timezone.now)
    type = models.PositiveSmallIntegerField(default=2, validators=[isValidType], help_text = "[('0', 'destroyed'), ('1', 'public'), ('2', 'private'), ('3', 'archived')]")
    status = models.CharField(
        max_length=2,
        choices=t_status,
        default='1',
        validators = [lambda v, t_status: v in [int(s[0]) for s in t_status]]
    )
    cover = models.ImageField(upload_to=cover_dir_path,blank=True, default='')
    logo = models.ImageField(upload_to=logo_dir_path,blank=True, default='')
    additional = models.JSONField(default = EmptyJson, null = True)

    def __str__(self) -> str:
        return self.name


class ServerAuthorizationLevel(models.Model):
    title = models.CharField(max_length = 128)
    description = models.CharField(max_length = 512, default = '')
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
    date_created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title


class ServerRole(models.Model):
    name = models.CharField(max_length = 64)
    server = models.ForeignKey(ToolServer, on_delete = models.CASCADE)
    description = models.CharField(max_length = 512, default = '')
    auth = models.ForeignKey(ServerAuthorizationLevel, on_delete = models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    def __str__(self) -> str:
        return f"{self.name} - {self.server}"


# Default to be role-based table
class UserServerAuthorization(models.Model):
    auth_type = models.ForeignKey(
        ServerAuthorizationLevel,
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
    role = models.ForeignKey(ServerRole, verbose_name=_("user role in the server"), on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user} in {self.server} : {self.role}"


class ToolAuthorizationLevel(models.Model):
    title = models.CharField(max_length = 128)
    description = models.CharField(max_length = 512, default = '')
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

    def __str__(self):
        return self.title
    

# Default to be role-based table
# Overwrite server-level ones, use as additional
class UserToolAuthorization(models.Model):
    auth_type = models.ForeignKey(
        ToolAuthorizationLevel,
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

    def __str__(self) -> str:
        return f"{self.user} in {self.tool.server}/{self.tool} : {self.role}"