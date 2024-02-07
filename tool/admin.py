from django.contrib import admin

# Register your models here.
from .models import ServerAuthorizationLevel, ToolAuthorizationLevel, Tool, ToolServer, ServerRole, UserServerAuthorization, UserToolAuthorization

admin.site.register(Tool)
admin.site.register(ToolServer)
admin.site.register(ServerAuthorizationLevel)
admin.site.register(ServerRole)
admin.site.register(UserServerAuthorization)
admin.site.register(ToolAuthorizationLevel)
admin.site.register(UserToolAuthorization)

