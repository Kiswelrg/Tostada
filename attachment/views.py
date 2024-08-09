from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.conf import settings
from django.http import HttpResponse, JsonResponse, FileResponse
from django.urls import reverse
from .models import MFile


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