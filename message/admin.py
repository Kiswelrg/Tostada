from django.contrib import admin
from .models import DirectMessage, GroupMessage

# Register your models here.
admin.site.register(DirectMessage)
admin.site.register(GroupMessage)