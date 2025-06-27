# Create your models here.
from django.db import models
import json
from django.utils import timezone
# from .util import getDirectMessageCode, getGroupMessageCode
from project.snowflake import getMessageMessageSnowflakeID
from django.core.exceptions import ValidationError


class Message(models.Model):
    contents = models.TextField(max_length=2000, blank=True, null=True)
    time_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    last_edit = models.DateTimeField(auto_now_add=True)
    _type = models.CharField(max_length=20, blank=True, null=True)
    urlCode = models.PositiveBigIntegerField(default=getMessageMessageSnowflakeID, unique=True, db_index=True, primary_key=True)

    class Meta:
        ordering = ['urlCode']
        # abstract = True


# Create your models here.
class DirectMessage(Message):
    sender = models.ForeignKey('account.AUser', on_delete=models.SET_NULL, related_name='sent_direct_messages2', null=True)
    receiver = models.ForeignKey('account.AUser', on_delete=models.SET_NULL, related_name='received_direct_messages2', null=True)

    class Meta:
        ordering = ['time_sent']
    def __str__(self):
        return ', '.join([c['content'] for c in json.loads(self.contents)])



class ChatMessage(models.Model):
    sender = models.ForeignKey('account.AUser', on_delete=models.SET_NULL, related_name='sent_group_messages2', null=True)
    receiver = models.ForeignKey('account.AUser', on_delete=models.SET_NULL, related_name='received_group_messages2', null=True, blank=True)
    mentioned_user = models.ForeignKey("account.AUser", on_delete=models.SET_NULL, related_name='mentioned_msgs2', null=True, blank=True)
    is_private = models.BooleanField(default=False)
    channel = models.ForeignKey("tool.ChannelOfChat", on_delete=models.SET_NULL, related_name='all_msgs', to_field='urlCode', null=True)
    tool_used = models.CharField(max_length=20, blank=True, null=True)
    
    contents = models.JSONField(blank=True, null=True)
    time_sent = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    last_edit = models.DateTimeField(auto_now_add=True, null=True)
    _type = models.CharField(max_length=20, blank=True, null=True)
    urlCode = models.PositiveBigIntegerField(default=getMessageMessageSnowflakeID, unique=True, db_index=True, primary_key=True)
    state = models.CharField(
        default='0',
        max_length=2,
        choices=[
            ('0', 'pending'),
            ('1', 'active'),
            ('2', 'archived')
        ],
        verbose_name = '''
        state:
        [
            ('0', 'pending'),
            ('1', 'active'),
            ('2', 'archived')
        ]
        '''
        )

    class Meta:
        ordering = ['urlCode']

    def clean(self):
        if not isinstance(self.contents, list):
            raise ValidationError("Only lists are allowed in the JSONField of the message's contents.")

    def __str__(self):
        result = ''
        for c in self.contents:
            result += str(c['content'])
        
        if len(result) <= 100:
            return result if len(result) > 0 else f'Message {self.urlCode}'
        else:
            return result[:97] + '...'
        