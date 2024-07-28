# Create your models here.
from django.db import models
import json
# from .util import getDirectMessageCode, getGroupMessageCode
from project.snowflake import getMessageDirectMessageSnowflakeID, getMessageGroupMessageSnowflakeID


class Message(models.Model):
    contents = models.JSONField(blank=True, null=True)
    time_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    last_edit = models.DateTimeField(auto_now_add=True)
    _type = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ['time_sent']
        abstract = True


# Create your models here.
class DirectMessage(Message):
    sender = models.ForeignKey('account.AUser', on_delete=models.SET_NULL, related_name='sent_direct_messages2', null=True)
    receiver = models.ForeignKey('account.AUser', on_delete=models.SET_NULL, related_name='received_direct_messages2', null=True)

    urlCode = models.PositiveBigIntegerField(default=getMessageDirectMessageSnowflakeID, unique=True, db_index=True, primary_key=True)

    class Meta:
        ordering = ['time_sent']
    def __str__(self):
        return ', '.join([c['content'] for c in json.loads(self.contents)])



class GroupMessage(Message):
    sender = models.ForeignKey('account.AUser', on_delete=models.SET_NULL, related_name='sent_group_messages2', null=True)
    receiver = models.ForeignKey('account.AUser', on_delete=models.SET_NULL, related_name='received_group_messages2', null=True, blank=True)
    mentioned_user = models.ForeignKey("account.AUser", on_delete=models.SET_NULL, related_name='mentioned_msgs2', null=True, blank=True)

    is_private = models.BooleanField(default=False)
    channel = models.ForeignKey("tool.ChannelOfChat", on_delete=models.SET_NULL, related_name='all_msgs', to_field='urlCode', null=True)
    tool_used = models.CharField(max_length=20, blank=True, null=True)
    urlCode = models.PositiveBigIntegerField(default=getMessageGroupMessageSnowflakeID, unique=True, db_index=True, primary_key=True)

    class Meta:
        ordering = ['time_sent']
    def __str__(self):
        return ', '.join([c['content'] for c in json.loads(self.contents)])