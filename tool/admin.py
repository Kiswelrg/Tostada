from django.contrib import admin

# Register your models here.
from .models import AuthorizationLevel, ToolServer, ServerRole, UserServerRole, UserToolRole
from .models import ToolOfInputAndOutput
from .models import CategoryInServer

admin.site.register(ToolOfInputAndOutput)
admin.site.register(ToolServer)
admin.site.register(CategoryInServer)
admin.site.register(AuthorizationLevel)
admin.site.register(ServerRole)
admin.site.register(UserServerRole)
admin.site.register(UserToolRole)

