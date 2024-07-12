from django.contrib import admin

# Register your models here.
from .models import AuthorizationLevel, Server, ServerRole, UserServerRole, UserChannelOfVoiceRole, UserChannelOfChatRole
from .models import ChannelOfChat, ChannelOfVoice
from .models import CategoryInServer

admin.site.register(ChannelOfChat)
admin.site.register(ChannelOfVoice)
admin.site.register(Server)
admin.site.register(CategoryInServer)
admin.site.register(AuthorizationLevel)
admin.site.register(ServerRole)
admin.site.register(UserServerRole)
admin.site.register(UserChannelOfChatRole)
admin.site.register(UserChannelOfVoiceRole)

