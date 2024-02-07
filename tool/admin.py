from django.contrib import admin

# Register your models here.
from .models import ServerAuthorizationLevels
from .models import ToolAuthorizationLevels

admin.site.register(ServerAuthorizationLevels)
admin.site.register(ToolAuthorizationLevels)

