from django.contrib import admin

# Register your models here.
from .models import ServerAuthorizationLevel, ToolAuthorizationLevel, ToolServer, ServerRole, UserServerAuthorization, UserToolAuthorization
from .models import ToolOfInputAndOutput


admin.site.register(ToolOfInputAndOutput)
admin.site.register(ToolServer)
admin.site.register(ServerAuthorizationLevel)
admin.site.register(ServerRole)
admin.site.register(UserServerAuthorization)
admin.site.register(ToolAuthorizationLevel)
admin.site.register(UserToolAuthorization)

