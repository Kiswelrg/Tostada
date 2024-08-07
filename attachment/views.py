from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.conf import settings
from django.http import HttpResponse, JsonResponse


# Create your views here.


@require_GET
def msg_attachment(request, channel_cid, attachment_cid, attachment_name, **kwargs):
    params = {
        'ex': [],
        'is': [],
        'hm': []
    }
    params.update(request.GET)
    if any([len(params[k])==0 for k in params]):
        return HttpResponse({
            'This content is no longer available.'
        })
    return JsonResponse({
        'args': params,
    })