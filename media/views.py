from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from tool.models import Server, UserServerRole
from account.models import AUser
from UtilGlobal.image.main import resize_image

# Create your views here.
def logo(request, server_cid, logo_name):
    s = get_object_or_404(Server, urlCode=server_cid, logo__exact=f'logo/{server_cid}/{logo_name}')
    size = request.GET.get('size', None)
    if size is None:
        return FileResponse(s.logo.file)
    else:
        return resize_image(s.logo.file, int(size))


def cover(request, server_cid, cover_name):
    s = get_object_or_404(Server, urlCode=server_cid, cover__exact=f'cover/{server_cid}/{cover_name}')
    size = request.GET.get('size', None)
    if size is None:
        return FileResponse(s.cover.file)
    else:
        return resize_image(s.cover.file, int(size))


def avatar(request, user_cid, avatar_name):
    u = get_object_or_404(AUser, urlCode=user_cid, avatar__exact=f'avatar/{user_cid}/{avatar_name}')
    size = request.GET.get('size', None)
    if size is None:
        return FileResponse(u.avatar.file)
    else:
        return resize_image(u.avatar.file, int(size))


def usercover(request, user_cid, usercover_name):
    u = get_object_or_404(AUser, urlCode=user_cid, cover__exact=f'usercover/{user_cid}/{usercover_name}')
    size = request.GET.get('size', None)
    if size is None:
        return FileResponse(u.cover.file)
    else:
        return resize_image(u.cover.file, int(size))

