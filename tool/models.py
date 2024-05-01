from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.dispatch import receiver
import os

from .util import model
# Create your models here.


def EmptyJson():
    return {}

def getDefaultAdditional():
    return {"type": "ToolTypical", "subclass":"ToolOfIO"}

class ToolServer(models.Model):
    def cover_dir_path(instance, filename):
        return f'cover/server-{instance.urlCode}/' + instance.date_created.strftime('%Y-%m-%d/' + filename)

    def logo_dir_path(instance, filename):
        return f'logo/server-{instance.urlCode}/' + instance.date_created.strftime('%Y-%m-%d/' + filename)

    ts_status = [
        ('0', 'destroyed'),
        ('1', 'public'),
        ('2', 'private'),
        ('3', 'archived'),
    ]
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank = True)
    urlCode = models.PositiveBigIntegerField(
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
        "account.AUser",
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
    additional = models.JSONField(default=getDefaultAdditional, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    def initDefaultRole(self):
        return ServerRole.objects.create(
                name = 'everyone',
                server = self
            )
        
    def initDefaultCategories(self, with_tool = False):
        names = [
            ('welcome', 'Hi'),
            ('chat', 'Main'),
            ('voice', 'General')
        ]
        data = {
            'categories': [
                CategoryInServer.objects.create(
                    name = name[0],
                    server = self
                ) for name in names
            ],
            
        }
        tools = [
                    ToolOfChat.objects.create(
                        name = names[i][1],
                        server = self,
                        category = data['categories'][i]
                    ) for i in range(3)
                ] if with_tool else []
        data['tools'] = tools
        return data

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
            # Init a Default Role called 'everyone'
            save_list = []
            role = self.initDefaultRole()
            ids = AuthorizationLevel.objects.filter(title__in = [name[0] for name in self.default_permissions_for_everyone])
            role.auth.set(ids)
            user_server_role = UserServerRole.objects.create(
                user = self.owner,
                server = self,
                role = role
            )
            save_list.append(user_server_role)
            save_list.append(role)

            # Init Default Categories: welcome, chat, voice
            cs = self.initDefaultCategories(with_tool=True)
            for c in cs['categories']:
                save_list.append(c)
            for t in cs['tools']:
                save_list.append(t)
            for item in save_list:
                item.save()

@receiver(models.signals.post_delete, sender=ToolServer)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MyModel` object is deleted.
    """
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)

@receiver(models.signals.pre_save, sender=ToolServer)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `ToolServer` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = ToolServer.objects.get(pk=instance.pk).logo
    except ToolServer.DoesNotExist:
        return False

    if old_file == '':
        return
    new_file = instance.logo
    
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class CategoryInServer(models.Model):
    name = models.CharField(max_length=100)
    server = models.ForeignKey(ToolServer, on_delete=models.CASCADE, related_name='categories')
    type = models.CharField(
        default='0',
        max_length=2,
        choices=[
            ('0', 'chat'),
            ('1', 'voice'),
        ],
        verbose_name = '''
        type:
        [
            ('0', 'chat'),
            ('1', 'voice'),
        ]
        '''
        )
    urlCode = models.PositiveBigIntegerField(default=model.getCategoryCode, unique=True, db_index=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} in {self.server}"


class Tool(models.Model):
    def cover_dir_path(instance, filename):
        return f'cover/tool-{instance.urlCode}/' + instance.date_created.strftime('%Y-%m-%d/' + filename)

    def logo_dir_path(instance, filename):
        return f'logo/tool-{instance.urlCode}/' + instance.date_created.strftime('%Y-%m-%d/' + filename)

    t_status = [
        ('0', 'destroyed'),
        ('1', 'public'),
        ('2', 'private'),
        ('3', 'archived'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank = True)

    urlCode = models.PositiveBigIntegerField(
        default=model.getToolCode, unique=True, db_index=True)
    date_created = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=2,
        choices=t_status,
        default='1',
        validators=[]
    )
    cover = models.ImageField(upload_to=cover_dir_path, blank=True, default='')
    logo = models.ImageField(upload_to=logo_dir_path, blank=True, default='')
    additional = models.JSONField(default=getDefaultAdditional, null=True, blank = True)

    def __str__(self) -> str:
        return f"{self.name} in {self.server}"
    

    class Meta:
        abstract = True


class ToolOfIO(Tool):
    category = models.ForeignKey(
        CategoryInServer,
        on_delete = models.CASCADE,
        related_name = 'toolofios',
    )
    server = models.ForeignKey(
        ToolServer, on_delete=models.CASCADE, related_name='toolofios')
    method_names = models.JSONField(default=EmptyJson, blank = True)
    input = models.JSONField(default=EmptyJson, null=True, blank = True)
    output = models.JSONField(default=EmptyJson, null=True, blank = True)


class ToolOfChat(Tool):
    category = models.ForeignKey(
        CategoryInServer,
        on_delete = models.CASCADE,
        related_name = 'toolofchats',
    )
    server = models.ForeignKey(
        ToolServer, on_delete=models.CASCADE, related_name='toolofchats')
    method_names = models.JSONField(default=EmptyJson, blank = True)
    bots = models.JSONField(default=EmptyJson, null=True, blank = True)


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
        'account.AUser',
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
    order = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user} in [{self.server} : {self.role.name}]"


# Default to be role-based table
class UserToolOfIORole(models.Model):
    user = models.ForeignKey(
        'account.AUser',
        on_delete=models.CASCADE,
        related_name='user_toolofio_auths'
    )
    tool = models.ForeignKey(
        ToolOfIO,
        on_delete=models.CASCADE,
        related_name='user_toolofio_auths'
    )
    role = models.ForeignKey(ServerRole, verbose_name=_(
        "user role in the server"),
        on_delete=models.CASCADE,
        related_name='user_toolofio_auths',
    )
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user} in .. 服务器: {self.tool.server} .. 工具: {self.tool.name} .. 角色: {self.role.name}"


class UserToolOfChatRole(models.Model):
    user = models.ForeignKey(
        'account.AUser',
        on_delete=models.CASCADE,
        related_name='user_toolofchat_auths'
    )
    tool = models.ForeignKey(
        ToolOfChat,
        on_delete=models.CASCADE,
        related_name='user_toolofchat_auths'
    )
    role = models.ForeignKey(ServerRole, verbose_name=_(
        "user role in the server"),
        on_delete=models.CASCADE,
        related_name='user_toolofchat_auths',
    )
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user} in .. 服务器: {self.tool.server} .. 工具: {self.tool.name} .. 角色: {self.role.name}"