from django.contrib import admin

# Register your models here.
from .models import AuthorizationLevel, Server, ServerRole, UserServerRole, UserChannelOfChatRole, UserChannelOfIORole
from .models import ChannelOfIO, ChannelOfChat
from .models import CategoryInServer

admin.site.register(ChannelOfIO)
admin.site.register(ChannelOfChat)
admin.site.register(Server)
admin.site.register(CategoryInServer)
admin.site.register(AuthorizationLevel)
admin.site.register(ServerRole)
admin.site.register(UserServerRole)
admin.site.register(UserChannelOfIORole)
admin.site.register(UserChannelOfChatRole)

