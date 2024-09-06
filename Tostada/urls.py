"""
URL configuration for Tostada project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.urls.conf import include
from django.http.response import HttpResponseRedirect
from account.views import Home
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # re_path(r'^ipa/(?P<path>.*)$', lambda request, path: HttpResponseRedirect(f'/static/{path}')),
    path('', Home),

    re_path(r'^(?:api/)?i/', include('tool.urls', namespace = 'tool')),
    re_path(r'^(?:api/)?account/', include('account.urls', namespace = 'account')),
    re_path(r'^(?:api/)?attachment/', include('attachment.urls', namespace = 'attachment')),
    path('favicon.svg', lambda request: HttpResponseRedirect('/static/favicon.svg')),
    path('favicon.ico', lambda request: HttpResponseRedirect('/static/favicon.svg')),


# this is for dev only, change before going to production
]


if settings.DEBUG:
    urlpatterns.extend(
        (
            static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + 
            static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        )
    )
