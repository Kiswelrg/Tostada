# Create your models here.
from django.db import models
import json
import re
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
    mentioned_users = models.ManyToManyField("account.AUser", related_name='mentioned_msgs2', blank=True)
    mentions_all = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    channel = models.ForeignKey("tool.ChannelOfChat", on_delete=models.SET_NULL, related_name='all_msgs', to_field='urlCode', null=True)
    tool_used = models.CharField(max_length=20, blank=True, null=True)
    
    contents = models.JSONField(default=dict, null=False)
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
    
    # Denormalized fields for search optimization
    content_text = models.TextField(max_length=4000, blank=True, db_index=True)
    has_text = models.BooleanField(default=False, db_index=True)
    has_link = models.BooleanField(default=False, db_index=True)
    has_mention = models.BooleanField(default=False, db_index=True)
    has_attachment = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ['urlCode']

    def _extract_content_info(self):
        """Extract denormalized fields from contents JSON"""
        if not isinstance(self.contents, dict):
            return
            
        content_list = self.contents.get('block', [])
        text_parts = []
        has_link = False
        has_mention = False
        has_attachment = False
        
        for block in content_list:
            if not isinstance(block, dict):
                continue
            
            type_content_key = {
                'text': 'content',
                'mention': 'content',
                'link': 'url',
                'attachment': 'content',
                'image': 'content',
                'file': 'content'
            }
            block_type = block.get('type', '')
            content = block.get(type_content_key[block_type], '')
            
            if block_type == 'text' and content:
                text_parts.append(str(content))
                # Check for URLs in text
                # if re.search(r'https?://[^\s]+', json.dumps(content)):
                #     has_link = True

            elif block_type == 'mention':
                has_mention = True
                if content:
                    text_parts.append(f"@{content}")
                    
            elif block_type == 'link':
                has_link = True
                if content:
                    text_parts.append(str(content))
                    
            elif block_type in ['attachment', 'image', 'file']:
                has_attachment = True
                if content:
                    text_parts.append(str(content))
        
        # Update denormalized fields
        self.content_text = ' '.join(text_parts)[:4000]  # Respect max_length
        self.has_text = len(text_parts) > 0
        self.has_link = has_link
        self.has_mention = has_mention or self.mentions_all
        self.has_attachment = has_attachment

    def clean(self):
        if not isinstance(self.contents, dict):
            raise ValidationError("Only dictionaries are allowed in the JSONField of the message's contents.")
        
        # Validate new format structure
        if 'version' not in self.contents or 'block' not in self.contents:
            raise ValidationError("Contents must have 'version' and 'block' fields.")
        
        if not isinstance(self.contents['block'], list):
            raise ValidationError("The 'block' field must be a list in the message's contents.")
    
    def save(self, *args, **kwargs):
        self._extract_content_info()
        super().save(*args, **kwargs)

    def __str__(self):
        result = ''
        
        # Process new format
        content_list = self.contents.get('block', [])
        
        for c in content_list:
            if isinstance(c, dict) and 'content' in c:
                result += str(c['content'])
        
        if len(result) <= 100:
            return result if len(result) > 0 else f'Message {self.urlCode}'
        else:
            return result[:97] + '...'
        