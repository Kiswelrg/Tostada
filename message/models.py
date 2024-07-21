# Create your models here.
from django.db import models
from .util import getDirectMessageCode, getGroupMessageCode


class Message(models.Model):
    content = models.TextField()
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
    sender = models.ForeignKey('account.AUser', on_delete=models.SET_NULL, related_name='sent_direct_messages', null=True)
    receiver = models.ForeignKey('account.AUser', on_delete=models.SET_NULL, related_name='received_direct_messages', null=True)
    urlCode = models.PositiveBigIntegerField(default=getDirectMessageCode, unique=True, db_index=True)

    class Meta:
        ordering = ['time_sent']
    def __str__(self):
        return self.msg_content



class GroupMessage(Message):
    sender = models.ForeignKey('account.AUser', on_delete=models.SET_NULL, related_name='sent_group_messages', null=True)
    receiver = models.ForeignKey('account.AUser', on_delete=models.SET_NULL, related_name='received_group_messages', null=True)
    mentioned_user = models.ForeignKey("account.Auser", on_delete=models.SET_NULL, related_name='mentioned_msgs', null=True)
    is_private = models.BooleanField(default=False)
    channel = models.ForeignKey("tool.ChannelOfChat", on_delete=models.SET_NULL, related_name='all_msgs', null=True)
    tool_used = models.CharField(max_length=20, blank=True, null=True)
    urlCode = models.PositiveBigIntegerField(default=getGroupMessageCode, unique=True, db_index=True)

    class Meta:
        ordering = ['time_sent']
    def __str__(self):
        return self.msg_content