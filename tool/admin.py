from django.contrib import admin

# Register your models here.
from .models import AuthorizationLevel, ToolServer, ServerRole, UserServerRole, UserToolRole
from .models import ToolOfIO, ToolOfChat
from .models import CategoryInServer
from .models import Tool

admin.site.register(Tool)
admin.site.register(ToolOfIO)
admin.site.register(ToolOfChat)
admin.site.register(ToolServer)
admin.site.register(CategoryInServer)
admin.site.register(AuthorizationLevel)
admin.site.register(ServerRole)
admin.site.register(UserServerRole)
admin.site.register(UserToolRole)

