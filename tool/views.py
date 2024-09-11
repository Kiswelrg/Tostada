from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import Server, ServerRole, UserServerRole, ChannelOfChat, ChannelOfVoice, CategoryInServer
from .models import UserChannelOfChatRole, UserChannelOfVoiceRole, AuthBits
from UtilGlobal.print import printc
from UtilGlobal.decorator.view_perm import require_login
from .util.ImportTool import import_function_from_file, importFunction
import json

tool_classes = [
    ChannelOfChat,
    ChannelOfVoice
]

tool_class_full = {
    'ChannelOfChat': ChannelOfChat,
    'ChannelOfVoice': ChannelOfVoice
}

tool_role_short = {
    'io': UserChannelOfChatRole,
    'chat': UserChannelOfVoiceRole
}

tool_class_short = {
    'io': ChannelOfChat,
    'chat': ChannelOfVoice
}



# Create your views here.
@require_login
def Home(request):
    return render(request, 'index.html')


# Fetch all tool servers that a user has joined
@require_login
def fetch_user_tool_servers(request):
    # tool_servers = Server.objects.filter(user_server_auths__user__urlCode=request.user.auser.urlCode)
    u = request.user.auser
    u_s_role = UserServerRole.objects.filter(user__urlCode=u.urlCode)
    data = [
        {
            "cid": str(us.role.server.urlCode),
            "name": us.role.server.name,
            "description": us.role.server.description,
            "logoSrc": '/media/default/server/logo/logo.svg' if us.role.server.logo == '' else us.role.server.logo.url,
            "order": us.order,
            "date_added": us.date_added.strftime("%Y-%m-%dT%H:%M:%SZ")
        } for us in u_s_role
    ]
    return JsonResponse({"tool_servers": data, 'r': True})


@require_login
@require_POST
def reorderServers(request):
    try:
        change_list = json.loads(request.POST['change_list'])
    except MultiValueDictKeyError:
        raise Http404('Damn')
    change_list = {int(s['cid']):s for s in change_list}

    # Verify user auth on every server in change_list
    u = request.user.auser
    if any(
        [not UserServerRole.objects.filter(user=u, role__server__urlCode=k).exists() for k in change_list]
    ):
        raise PermissionDenied

    # Search targetted servers
    r = UserServerRole.objects.filter(user__urlCode = u.urlCode, role__server__urlCode__in = change_list.keys())
    for u_s_r in r:
        if u_s_r.order != change_list[u_s_r.role.server.urlCode]['old_order']:
            raise Http404('Damn')
        u_s_r.order = change_list[u_s_r.role.server.urlCode]['order']
        u_s_r.save()
    return JsonResponse({'msg': 'reorder success','r': True})


@require_login
def reorderServerCategorys(request):
    try:
        change_list = json.loads(request.POST['change_list'])
    except MultiValueDictKeyError:
        raise Http404('Damn')
    change_list = {int(c['cid']):c for c in change_list}

    # Verify change_list
    if len(change_list) != 2:
        raise PermissionDenied
    else:
        ks = list(change_list.keys())
        # category not exist
        if any(
            [not CategoryInServer.objects.filter(urlCode=cid).exists() for cid in ks]
        ):
            raise PermissionDenied
        # does not belong to the same server
        server0 = CategoryInServer.objects.get(urlCode=ks[0]).server
        if server0 != CategoryInServer.objects.get(urlCode=ks[1]).server:
            raise PermissionDenied
        # user has auth
        hasAuth = False
        for auth in ServerRole.objects.filter(server=server0, user_server_auths__user=request.user.auser):
            v = auth.auth_value
            if (v & AuthBits['Manage Channels'] > 0) or (v & AuthBits['Administrator'] > 0):
                hasAuth = True
                break
        if not hasAuth: raise PermissionDenied

    # Search target categories
    u = request.user.auser
    r = CategoryInServer.objects.filter(server__owner__urlCode = u.urlCode, urlCode__in = change_list.keys())
    print(change_list)
    for c_in_s in r:
        if c_in_s.order != change_list[c_in_s.urlCode]['old_order']:
            raise Http404('Damn')
        c_in_s.order = change_list[c_in_s.urlCode]['order']
        c_in_s.save()
    return JsonResponse({'msg': 'reorder success','r': True})


# Fetch a specific tool server by its urlCode
@require_login
def fetch_tool_server(request, tool_server_code):
    u = request.user.auser
    tool_server = get_object_or_404(Server, urlCode=tool_server_code)
    tools = {}
    data = {
        "cid": str(tool_server.urlCode),
        "name": tool_server.name,
        "description": tool_server.description,
        "status": tool_server.get_status_display(),
        "type": tool_server.get_type_display(),
        "date_created": tool_server.date_created.date(),
    }

    if 'tools' not in request.GET or not request.GET['tools'] == '1':
        return JsonResponse({"tool_server": data, "r": True, "type": "no-tool"})
    
    if UserServerRole.objects.filter(user__urlCode=u.urlCode, role__server = tool_server).exists():
        # If already a member of the server, (return all types of tools)
        for k, v in tool_class_short.items():
            tools[k] = v.objects.filter(server=tool_server)
    # No direct access to the whole server
    else:
        for k, v in tool_role_short.items():
            tool_querys = v.objects.filter(
            user__urlCode=u.urlCode,
            tool__server=tool_server
            ).values_list('tool', flat=True)

            # Get the corresponding tool objects
            if tool_querys.exists():
                tools[k] = tool_class_short[k].objects.filter(id__in=tool_querys)
        
    
    category_dict = {}
    for k, tool_set in tools.items():
        for tool in tool_set:
            t = {
                "cid": str(tool.urlCode),
                "name": tool.name,
                "description": tool.description,
                "isServerEntry": tool.isServerEntry,
                "sub_class": k,
                "category": {
                    'type': tool.category.get_type_display(),
                    'order': tool.category.order,
                    'cid': str(tool.category.urlCode)
                }
            }
            if tool.category.name not in category_dict:
                category_dict[tool.category.name] = {
                    'tools': [t],
                    'order': tool.category.order,
                    'cid': str(tool.category.urlCode)
                }
            else:
                category_dict[tool.category.name]['tools'].append(t)

    print(category_dict)
    if tools and len(tools):
        data["category"] = category_dict
    else:
        print('no joined server/available tool')
    return JsonResponse({"tool_server": data, "r": True, "type": "with-tool"})


# Fetch a specific tool by its urlCode
@require_login
def fetch_tool(request, tool_class, tool_code):
    Sub_Tool = tool_class_short[tool_class]
    tool = get_object_or_404(Sub_Tool, urlCode=tool_code)
    
    # check auth
    u = request.user.auser
    if not UserServerRole.objects.filter(role__server=tool.server, user__urlCode=u.urlCode).exists():
        if not tool_role_short[tool_class].objects.filter(user__urlCode=u.urlCode, tool=tool).exists():
            return JsonResponse({"r": False})
        
    
    data = {
        "cid": str(tool.urlCode),
        "name": tool.name,
        "description": tool.description,
        "status": tool.get_status_display(),
        "date_created": tool.date_created.date(),
        "server": tool.server.name,
        "category": tool.category.name,
        "additional": tool.additional,
        "class": Sub_Tool.__name__
    }
    if 'sub_class' not in tool.additional:
        pass
    elif Sub_Tool.__name__ == 'ChannelOfChat':
        tool_specific = get_object_or_404(ChannelOfChat, pk = tool.pk)
        data['methods'] = tool_specific.method_names
    elif Sub_Tool.__name__ == 'ChannelOfVoice':
        pass
    return JsonResponse({"tool": data, "r": True})


# @require_POST
# @require_login
def run_tool(request, tool_code):
    printc([request.POST, tool_code], isList=True, color=[255,255,0])
    tool_class = request.POST['sub_class']
    tool_model = tool_class_full[tool_class]
    tool = tool_model.objects.filter(urlCode=tool_code)
    u = request.user.auser
    if not tool.exists():
        raise PermissionDenied
    else:
        tool = tool[0]
        roles = ServerRole.objects.filter(user_server_auths__user=u, server=tool.server)
        if not roles.exists():
            raise PermissionDenied
        hasAuth = False
        for r in roles:
            v = r.auth_value
            if (v & AuthBits['Manage Channels'] > 0) or (v & AuthBits['Administrator'] > 0):
                hasAuth = True
                break
        if not hasAuth: raise PermissionDenied


    methods = (tool_model.objects.get(urlCode = tool_code).method_names)
    method_detail = None
    for g in methods['groups']:
        for m in g['methods']:
            if m['code'] == int(request.POST['method-code']):
                method_detail = m
                break
        if method_detail:
            break
    if method_detail is None:
        raise Http404()
    name = method_detail.get('function_name')
    if name is None or len(name) == 0:
        name = request.POST['method-code']
    f_name = 'f_' + name
    f = importFunction(f'tool.servers.{methods["tool"]}.main', f_name)

    # 不具备复用
    r = f(method_detail, u, tool_code)
    return JsonResponse({
        'status': 200,
        'r': True,
        'msg': f'{tool_code} got!',
        'data': r
    })