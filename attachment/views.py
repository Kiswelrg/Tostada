from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.conf import settings
from django.http import HttpResponse, JsonResponse, FileResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http.response import Http404
from django.core.exceptions import PermissionDenied
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import MFile
from message.models import ChatMessage
from tool.models import ChannelOfChat, UserServerRole
from UtilGlobal.decorator.view_perm import require_login

# Create your views here.


@require_GET
def msg_attachment(request, channel_cid, attachment_cid, attachment_name, **kwargs):
    params = {
        'ex': '',
        'is': '',
        'hm': ''
    }
    params.update(request.GET)
    params = {k: params[k][0] for k in params}
    if any([len(params[k])==0 for k in params]):
        return HttpResponse({
            'This content is no longer available.'
        })
    v = MFile.validateURL(f"{channel_cid}/{attachment_cid}/{attachment_name}", args = params)
    if v:
        return FileResponse(MFile.objects.get(pk=attachment_cid).file)
    return HttpResponse({
            'This content is no longer available.'
        })



MAX_FILE_SIZE = 512 * 1024 * 1024  # 512 MB in bytes
@require_POST
@require_login
def upload_msg_attachment(request, channel_cid):
    files = request.FILES.getlist('files')
    
    if len(files) > 10:
        return JsonResponse({'error': 'No more than 10 files are allowed.'}, status=400)
    if sum([f.size for f in files]) > MAX_FILE_SIZE:
            return JsonResponse({'error': f'File "{file.name}" exceeds the size limit of 512 MB.'}, status=400)

    c = get_object_or_404(ChannelOfChat, urlCode=channel_cid)
    usrs = UserServerRole.objects.filter(role__server=c.server, user=request.user.auser)
    if not usrs.exists():
        raise Http404
    else:
        hasAuth = False
        for usr in usrs:
            v = usr.role.auth_value
            if (v & (0b1<<19 | 0b1<<44)) > 0:
                hasAuth = True
                break
        if not hasAuth: raise PermissionDenied

    uploaded_files_ids = []

    # Process each file
    msg = ChatMessage(
        sender=request.user.auser,
        is_private=False,
        channel=c,
        _type='normal',
        contents='',
        state='0'
    )
    msg.full_clean()
    msg.save()
    for file in files:
        # Create and save AFile object
        
        a_file = MFile.objects.create(
            _type=file.content_type,
            message=msg,
            file=file  # This saves the file to the storage (e.g., file system)
        )
        uploaded_files_ids.append(str(a_file.urlCode))

    return JsonResponse({
        'message': 'Files uploaded successfully',
        'file_ids': uploaded_files_ids
    })


def delete_msg_attachment(request, attach_cid):
    atm = get_object_or_404(MFile, urlCode=attach_cid)
    coc = atm.message.channel
    u = request.user.auser
    res = JsonResponse({
            'message': 'Attachment deleted',
            'r': True
        })
    channel_layer = get_channel_layer()
    consumer_channel_msg = {
        'type': 'attachment_deleted',
        'message': {}
    }
    if atm.message.sender == u:
        atm.delete()
        async_to_sync(channel_layer.group_send)(
            f'chat_{coc.urlCode}',  # Channel name/group
            consumer_channel_msg  # Message data
        )
        return res

    usrs = UserServerRole.objects.filter(role__server=coc.server, user=request.user.auser)
    if not usrs.exists():
        raise Http404
    else:
        hasAuth = False
        for usr in usrs:
            v = usr.role.auth_value
            if (v & (0b1<<24 | 0b1<<44)) > 0:
                hasAuth = True
                break
        if not hasAuth: raise PermissionDenied


    # hasAuth is True
    atm.delete()
    async_to_sync(channel_layer.group_send)(
        f'chat_{coc.urlCode}',  # Channel name/group
        consumer_channel_msg  # Message data
    )
    return res