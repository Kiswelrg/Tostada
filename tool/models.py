from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

from .util import model
# Create your models here.


def EmptyJson():
    return {}


class ToolServer(models.Model):
    def cover_dir_path(instance, filename):
        return f'cover/server-{instance.id}/' + instance.date_created.strftime('%Y-%m-%d/' + filename)

    def logo_dir_path(instance, filename):
        return f'logo/server-{instance.id}/' + instance.date_created.strftime('%Y-%m-%d/' + filename)

    ts_status = [
        ('0', 'destroyed'),
        ('1', 'public'),
        ('2', 'private'),
        ('3', 'archived'),
    ]
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank = True)
    urlCode = models.IntegerField(
        default=model.getToolServerCode, unique=True, db_index=True)
    date_created = models.DateTimeField(default=timezone.now)
    type = models.CharField(
        default='0',
        max_length=2,
        choices=[
            ('0', 'tool'),
            ('1', 'have fun'),
            ('2', 'others')
        ],
        verbose_name = '''
        type:
        [
            ('0', 'tool'),
            ('1', 'have fun'),
            ('2', 'others')
        ]
        '''
        )
    owner = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name='tool_servers'
    )
    status = models.CharField(
        max_length=2,
        choices=ts_status,
        default='1'
    )
    cover = models.ImageField(upload_to=cover_dir_path, blank=True, default='')
    logo = models.ImageField(upload_to=logo_dir_path, blank=True, default='')
    additional = models.JSONField(default={"type": {}}, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    default_permissions_for_everyone = [('View Channel',),
                ('Create Expressions',),
                ('Create Invite',),
                ('Change Nickname',),
                ('Send Messages',),
                ('Send Messages in Threads',),
                ('Create Public Threads',),
                ('Create Private Threads',),
                ('Embed Links',),
                ('Attach Files',),
                ('Add Reactions',),
                ('Use External Emoji',),
                ('Use External Stickers',),
                ('Mention @everyone, @here, and All Roles',),
                ('Read Message History',),
                ('Use Application Commands',),
                ('Send Voice Messages',),
                ('Connect',),
                ('Speak',),
                ('Video',),
                ('Use Activities',),
                ('Use Soundboard',),
                ('Use External Sounds',),
                ('Use Voice Activity',),
                ('Set Voice Channel Status',),
                ('Create Events',)
            ]
    def save(self, *args, **kwargs):
        isNew = self._state.adding
        super().save(*args, **kwargs)
        if isNew:
            
            ids = AuthorizationLevel.objects.filter(title__in = [name[0] for name in self.default_permissions_for_everyone])
            role = ServerRole.objects.create(
                name = 'everyone',
                server = self
            )
            role.auth.set(ids)
            role.save()

class CategoryInServer(models.Model):
    name = models.CharField(max_length=100)
    server = models.ForeignKey(ToolServer, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return f"{self.name} in {self.server}"

class Tool(models.Model):

    def cover_dir_path(instance, filename):
        return f'cover/tool-{instance.id}/' + instance.date_created.strftime('%Y-%m-%d/' + filename)

    def logo_dir_path(instance, filename):
        return f'logo/tool-{instance.id}/' + instance.date_created.strftime('%Y-%m-%d/' + filename)

    t_status = [
        ('0', 'destroyed'),
        ('1', 'public'),
        ('2', 'private'),
        ('3', 'archived'),
    ]

    server = models.ForeignKey(
        ToolServer, on_delete=models.CASCADE, related_name='tools')
    name = models.CharField(max_length=255)
    description = models.TextField(blank = True)

    urlCode = models.IntegerField(
        default=model.getToolCode, unique=True, db_index=True)
    date_created = models.DateTimeField(default=timezone.now)
    # type = models.CharField(
    #     default='0',
    #     max_length=2,
    #     choices=[
    #         ('0', 'blank'),
    #         ('1', 'intput & output'),
    #         ('2', 'exhibition'),
    #         ('3', 'blog')
    #     ])
    category = models.ForeignKey(
        CategoryInServer,
        on_delete = models.CASCADE,
        related_name = 'tools',
    )
    status = models.CharField(
        max_length=2,
        choices=t_status,
        default='1',
        validators=[]
    )
    cover = models.ImageField(upload_to=cover_dir_path, blank=True, default='')
    logo = models.ImageField(upload_to=logo_dir_path, blank=True, default='')
    additional = models.JSONField(default={"type": "ToolTypical"}, null=True, blank = True)

    def __str__(self) -> str:
        return f"{self.name} in {self.server}"


class ToolOfInputAndOutput(Tool):
    method_names = models.JSONField(default=EmptyJson, blank = True)
    input = models.JSONField(default=EmptyJson, null=True, blank = True)
    output = models.JSONField(default=EmptyJson, null=True, blank = True)
    

class AuthorizationLevel(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512, default='')
    type = models.CharField(
        max_length=2,
        default='0',
        choices=[
            ('0', 'binary'),
        ])
    category = models.CharField(
        max_length=3,
        default='0',
        choices=[
            ('0', 'General Server Permissions'),
            ('1', 'Membership PERMISSIONS'),
            ('2', 'TEXT CHANNEL PERMISSIONS'),
            ('3', 'VOICE CHANNEL PERMISSIONS'),
            ('4', 'EVENTS PERMISSIONS'),
            ('5', 'ADVANCED PERMISSIONS'),
        ])
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class ServerRole(models.Model):
    name = models.CharField(max_length=64)
    server = models.ForeignKey(
        ToolServer, on_delete=models.CASCADE, related_name='server_roles')
    description = models.CharField(max_length=512, default='')
    auth = models.ManyToManyField(
        AuthorizationLevel, related_name='server_roles')
    auth_value = models.BooleanField(default = True)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.name} - {self.server}"


# Default to be role-based table
class UserServerRole(models.Model):
    # auth_type = models.ForeignKey(
    #     AuthorizationLevel,
    #     on_delete=models.CASCADE,
    #     related_name='user_server_auths'
    # )
    # auth_value_bool = models.BooleanField(default=False)
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user_server_auths'
    )
    server = models.ForeignKey(
        ToolServer,
        on_delete=models.CASCADE,
        related_name='user_server_auths'
    )
    role = models.ForeignKey(ServerRole, verbose_name=_(
        "user role in the server"), on_delete=models.CASCADE, related_name='user_server_auths')
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user} in [{self.server} : {self.role.name}]"


# class ToolAuthorizationLevel(models.Model):
#     title = models.CharField(max_length=128)
#     description = models.CharField(max_length=512, default='')
#     type = models.CharField(
#         max_length=2,
#         default='0',
#         choices=[
#             ('0', 'binary'),
#         ])
#     category = models.CharField(
#         max_length=2,
#         default='0',
#         choices=[
#             ('0', 'General Tool Permissions'),
#             ('1', 'Membership Permissions'),
#             ('2', 'Other Permissions'),
#         ])
#     date_created = models.DateTimeField(default=timezone.now)

#     def __str__(self):
#         return self.title


# Default to be role-based table
# Overwrite server-level ones, use as additional
class UserToolRole(models.Model):
    # auth_type = models.ForeignKey(
    #     AuthorizationLevel,
    #     on_delete=models.CASCADE,
    #     related_name='user_tool_auths'
    # )
    # auth_value_bool = models.BooleanField(default=False)
    user = models.ForeignKey(
        'user.User',
        on_delete=models.CASCADE,
        related_name='user_tool_auths'
    )
    tool = models.ForeignKey(
        Tool,
        on_delete=models.CASCADE,
        related_name='user_tool_auths'
    )
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user} in [{self.tool.server}/{self.tool} : {self.role.name}]"
