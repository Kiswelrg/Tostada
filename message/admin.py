from django.contrib import admin
from .models import DirectMessage, ChatMessage

# Register your models here.
admin.site.register(DirectMessage)
admin.site.register(ChatMessage)