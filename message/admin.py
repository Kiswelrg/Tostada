from django.contrib import admin
from .models import DirectMessage, ChatMessage
from attachment.models import MFile

class MFileInline(admin.TabularInline):  # or use admin.StackedInline for a different layout
    model = MFile
    extra = 0  # No extra empty forms by default

@admin.register(ChatMessage)
class AAdmin(admin.ModelAdmin):
    inlines = [MFileInline]

# Register your models here.
# admin.site.register(ChatMessage)
admin.site.register(DirectMessage)