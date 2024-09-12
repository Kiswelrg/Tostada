from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.dispatch import receiver
from project.snowflake import getToolServerSnowflakeID, getToolChannelSnowflakeID, getToolCategoryInServerSnowflakeID
import os
from django.conf import settings
from hashlib import md5
from UtilGlobal.validator.FieldFile import imagefile_validator
from media.models import MediaFileSystemStorage
from .util import model
# Create your models here.

AuthBits = {
    'View Channel': 1,#0b1<<0
    'Manage Channels': 2,
    'Manage Roles': 4,
    'Create Expressions': 8,
    'Manage Expressions': 16,
    'View Audit Log': 32,#0b1<<5
    'Manage Webhooks': 64,
    'Manage Server': 128,
    'Create Invite': 256,
    'Change Nickname': 512,
    'Manage Nicknames': 1024,#0b1<<10
    'Kick Members': 2048,
    'Ban Members': 4096,
    'Timeout Members': 8192,
    'Send Messages': 16384,
    'Send Messages in Threads': 32768,#0b1<<15
    'Create Public Threads': 65536,
    'Create Private Threads': 131072,
    'Embed Links': 262144,
    'Attach Files': 524288,
    'Add Reactions': 1048576,#0b1<<20
    'Use External Emoji': 2097152,
    'Use External Stickers': 4194304,
    'Mention @everyone, @here, and All Roles': 8388608,
    'Manage Messages': 16777216,
    'Manage Threads': 33554432,#0b1<<25
    'Read Message History': 67108864,
    'Send Text-to-Speech Messages': 134217728,
    'Use Application Commands': 268435456,
    'Send Voice Messages': 536870912,
    'Connect': 1073741824,#0b1<<30
    'Speak': 2147483648,
    'Video': 4294967296,
    'Use Activities': 8589934592,
    'Use Soundboard': 17179869184,
    'Use External Sounds': 34359738368,#0b1<<35
    'Use Voice Activity': 68719476736,
    'Priority Speaker': 137438953472,
    'Mute Members': 274877906944,
    'Deafen Members': 549755813888,
    'Move Members': 1099511627776,#0b1<<40
    'Set Voice Channel Status': 2199023255552,
    'Create Events': 4398046511104,
    'Manage Events': 8796093022208,
    'Administrator': 17592186044416,#0b1<<44
}

def EmptyJson():
    return {}

def getDefaultAdditional():
    return {"type": "ToolTypical", "subclass":"ChannelOfChat"}

class Server(models.Model):
    @staticmethod
    def md5_filename(n):
        s = os.path.splitext(n)
        return md5(s[0].encode('utf-8')).hexdigest() + s[1]
    
    def cover_dir_path(instance, filename):
        return f'cover/{instance.urlCode}/' + Server.md5_filename(filename)

    def logo_dir_path(instance, filename):
        return f'logo/{instance.urlCode}/' + Server.md5_filename(filename)

    ts_status = [
        ('0', 'destroyed'),
        ('1', 'public'),
        ('2', 'private'),
        ('3', 'archived'),
    ]
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank = True)
    urlCode = models.PositiveBigIntegerField(
        default=getToolServerSnowflakeID, unique=True, db_index=True, primary_key=True)
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
    cover = models.ImageField(upload_to=cover_dir_path, blank=True, default='', validators=[imagefile_validator], storage=MediaFileSystemStorage)
    logo = models.ImageField(upload_to=logo_dir_path, blank=True, default='', validators=[imagefile_validator], storage=MediaFileSystemStorage)
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
            ('welcome', 'Hi', ChannelOfChat),
            ('chat', 'Main', ChannelOfChat),
            ('voice', 'General', ChannelOfVoice)
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
                    names[i][2].objects.create(
                        name = names[i][1],
                        server = self,
                        category = data['categories'][i]
                    ) for i in range(3)
                ] if with_tool else []
        tools[0].isServerEntry = True
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

    class Meta:
        ordering = ['urlCode']



class CategoryInServer(models.Model):
    name = models.CharField(max_length=100)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='categories', to_field='urlCode', null=True)
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
    urlCode = models.PositiveBigIntegerField(default=getToolCategoryInServerSnowflakeID, unique=True, db_index=True, primary_key=True)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} in {self.server}"


# Abstract Class
class Channel(models.Model):
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
    isServerEntry = models.BooleanField(default=False)
    
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


@receiver(models.signals.post_delete, sender=Server)
@receiver(models.signals.post_delete, sender=Channel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MyModel` object is deleted.
    """
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)
    if instance.cover:
        if os.path.isfile(instance.cover.path):
            os.remove(instance.logo.path)

@receiver(models.signals.pre_save, sender=Server)
@receiver(models.signals.pre_save, sender=Channel)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Server` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_files = [Server.objects.get(pk=instance.pk).logo,
                    Server.objects.get(pk=instance.pk).cover]
    except Server.DoesNotExist:
        return False

    if all([f == '' for f in old_files]) == '':
        return
    new_files = [
        instance.logo,
        instance.cover
    ]
    
    for i in range(len(old_files)):
        old_file = old_files[i]
        new_file = new_files[i]
        if not old_file == new_file:
            if old_file and os.path.isfile(old_file.path):
                os.remove(old_file.path)


class ChannelOfChat(Channel):
    urlCode = models.PositiveBigIntegerField(
        default=getToolChannelSnowflakeID, unique=True, db_index=True, primary_key=True)
    category = models.ForeignKey(
        CategoryInServer,
        on_delete = models.CASCADE,
        related_name = 'channelofchats',
        to_field='urlCode',
        null=True
    )
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name='channelofchats', to_field='urlCode', null=True)
    is_dm = models.BooleanField(default=False)
    method_names = models.JSONField(default=EmptyJson, blank = True)
    inputs = models.JSONField(default=EmptyJson, null=True, blank = True)
    outputs = models.JSONField(default=EmptyJson, null=True, blank = True)

    class Meta:
        ordering = ['urlCode']


class ChannelOfVoice(Channel):
    urlCode = models.PositiveBigIntegerField(
        default=getToolChannelSnowflakeID, unique=True, db_index=True, primary_key=True)
    category = models.ForeignKey(
        CategoryInServer,
        on_delete = models.CASCADE,
        related_name = 'channelofvoices',
        to_field='urlCode',
        null=True
    )
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name='channelofvoices', to_field='urlCode', null=True)
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
        Server, on_delete=models.CASCADE, related_name='server_roles', to_field='urlCode', null=True)
    description = models.CharField(max_length=512, default='', null=True, blank=True)
    # auth = models.ManyToManyField(
        # AuthorizationLevel, related_name='server_roles')
    auth_value = models.PositiveBigIntegerField(default = 0b0)
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
    nickname = models.CharField(max_length=64, blank=True)
    # server = models.ForeignKey(
    #     Server,
    #     on_delete=models.CASCADE,
    #     related_name='user_server_auths',
    #     to_field='urlCode',
    #     null=True
    # )
    role = models.ForeignKey(ServerRole, verbose_name=_(
        "user role in the server"), on_delete=models.CASCADE, related_name='user_server_auths')
    date_added = models.DateTimeField(default=timezone.now)
    order = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user} in [{self.role.server} : {self.role.name}]"


# Default to be role-based table
class UserChannelOfChatRole(models.Model):
    user = models.ForeignKey(
        'account.AUser',
        on_delete=models.CASCADE,
        related_name='user_channelofchat_auths'
    )
    channel = models.ForeignKey(
        ChannelOfChat,
        on_delete=models.CASCADE,
        related_name='user_channelofchat_auths'
    )
    role = models.ForeignKey(ServerRole, verbose_name=_(
        "user role in the server"),
        on_delete=models.CASCADE,
        related_name='user_channelofchat_auths',
    )
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user} in .. 服务器: {self.tool.server} .. 工具: {self.tool.name} .. 角色: {self.role.name}"


class UserChannelOfVoiceRole(models.Model):
    user = models.ForeignKey(
        'account.AUser',
        on_delete=models.CASCADE,
        related_name='user_channelofvoice_auths'
    )
    channel = models.ForeignKey(
        ChannelOfVoice,
        on_delete=models.CASCADE,
        related_name='user_channelofvoice_auths'
    )
    role = models.ForeignKey(ServerRole, verbose_name=_(
        "user role in the server"),
        on_delete=models.CASCADE,
        related_name='user_channelofvoice_auths',
    )
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"{self.user} in .. 服务器: {self.tool.server} .. 工具: {self.tool.name} .. 角色: {self.role.name}"
    


