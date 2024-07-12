from django.db import models

# Create your models here.
class Msg(models.Model):
    content = models.TextField(blank=True, null=True)
    _type = models.CharField(max_length=20, blank=True, null=True)
    sent_time = models.DateTimeField(blank=True, null=True)
    last_edit = models.DateTimeField(blank=True, null=True)
    from_user = models.ForeignKey("account.Auser", on_delete=models.SET_NULL, related_name='sent_msgs', null=True)
    mentioned_user = models.ForeignKey("account.Auser", on_delete=models.SET_NULL, related_name='mentioned_msgs', null=True)
    edited = models.BooleanField(default=False)
    self_seen = models.BooleanField(default=False)
    channel = models.ForeignKey("tool.ChannelOfChat", on_delete=models.SET_NULL, related_name='all_msgs', null=True)
    
    def __str__(self):
        return self.msg_content
    
    