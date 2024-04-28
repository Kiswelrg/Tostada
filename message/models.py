from django.db import models


class Message(models.Model):
    content = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_edited = models.BooleanField(default=False)
    last_modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_sent']


# Create your models here.
class DirectMessage(Message):
    sender = models.ForeignKey('account.AUser', on_delete=models.CASCADE, related_name='sent_direct_messages')
    receiver = models.ForeignKey('account.AUser', on_delete=models.CASCADE, related_name='received_direct_messages')

    class Meta:
        ordering = ['date_sent']



class GroupMessage(Message):
    sender = models.ForeignKey('account.AUser', on_delete=models.CASCADE, related_name='sent_group_messages')
    
    is_private = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_sent']