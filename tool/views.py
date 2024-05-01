from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import Http404
from django.utils.datastructures import MultiValueDictKeyError
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import ToolServer, UserServerRole, UserToolOfIORole, UserToolOfChatRole, ToolOfIO, ToolOfChat, CategoryInServer
from UtilGlobal.print import printc
from .util.ImportTool import import_function_from_file, importFunction
import json

tool_classes = [
    ToolOfIO,
    ToolOfChat
]

tool_class_full = {
    'ToolOfIO': ToolOfIO,
    'ToolOfChat': ToolOfChat
}

tool_role_short = {
    'io': UserToolOfIORole,
    'chat': UserToolOfChatRole
}

tool_class_short = {
    'io': ToolOfIO,
    'chat': ToolOfChat
}



# Create your views here.
def Home(request):
    return render(request, 'index.html')


# Fetch all tool servers that a user has joined
def fetch_user_tool_servers(request):
    # tool_servers = ToolServer.objects.filter(user_server_auths__user__username=request.session['username'])
    u_s_role = UserServerRole.objects.filter(user__username=request.session['username'])
    data = [
        {
            "cid": str(us.server.urlCode),
            "name": us.server.name,
            "description": us.server.description,
            "logoSrc": '/media/default/server/logo/logo.svg' if us.server.logo == '' else us.server.logo.url,
            "order": us.order,
            "date_added": us.date_added.strftime("%Y-%m-%dT%H:%M:%SZ")
        } for us in u_s_role
    ]
    return JsonResponse({"tool_servers": data, 'r': True})

@require_POST
def reorderServers(request):
    try:
        change_list = json.loads(request.POST['change_list'])
    except MultiValueDictKeyError:
        raise Http404('Damn')
    change_list = {int(s['cid']):s for s in change_list}
    # Verify user auth

    # use custom decorator to check if logged in

    # Search targetted servers
    r = UserServerRole.objects.filter(user__username = request.session['username'], server__urlCode__in = change_list.keys())
    print(change_list)
    for u_s_r in r:
        if u_s_r.order != change_list[u_s_r.server.urlCode]['old_order']:
            raise Http404('Damn')
        u_s_r.order = change_list[u_s_r.server.urlCode]['order']
        u_s_r.save()
    return JsonResponse({'msg': 'reorder success','r': True})


def reorderServerCategorys(request):
    try:
        change_list = json.loads(request.POST['change_list'])
    except MultiValueDictKeyError:
        raise Http404('Damn')
    change_list = {int(c['cid']):c for c in change_list}
    # Verify user auth

    # use custom decorator to check if logged in

    # Search targetted servers
    r = CategoryInServer.objects.filter(server__owner__username = request.session['username'], urlCode__in = change_list.keys())
    print(change_list)
    for c_in_s in r:
        if c_in_s.order != change_list[c_in_s.urlCode]['old_order']:
            raise Http404('Damn')
        c_in_s.order = change_list[c_in_s.urlCode]['order']
        c_in_s.save()
    return JsonResponse({'msg': 'reorder success','r': True})


# Fetch a specific tool server by its urlCode
def fetch_tool_server(request, tool_server_code):
    tool_server = get_object_or_404(ToolServer, urlCode=tool_server_code)
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
    
    if UserServerRole.objects.filter(user__username=request.session['username'], server = tool_server).exists():
        # If already a member of the server, (return all types of tools)
        for k, v in tool_class_short.items():
            tools[k] = v.objects.filter(server=tool_server)
    # No direct access to the whole server
    else:
        for k, v in tool_role_short.items():
            tool_querys = v.objects.filter(
            user__username=request.session['username'],
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
def fetch_tool(request, tool_class, tool_code):
    Sub_Tool = tool_class_short[tool_class]
    tool = get_object_or_404(Sub_Tool, urlCode=tool_code)
    # user_tool = None

    if not UserServerRole.objects.filter(server=tool.server, user__username=request.session['username']).exists():
        if not tool_role_short[tool_class].objects.filter(user__username=request.session['username'], tool=tool).exists():
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
    elif Sub_Tool.__name__ == 'ToolOfIO':
        tool_specific = get_object_or_404(ToolOfIO, id = tool.id)
        data['methods'] = tool_specific.method_names
    elif Sub_Tool.__name__ == 'ToolOfChat':
        pass
    return JsonResponse({"tool": data, "r": True})


@require_POST
def run_tool(request, tool_code):
    printc([request.POST, tool_code], isList=True, color=[255,255,0])
    tool_class = request.POST['sub_class']
    # add = Tool.objects.get(urlCode = tool_code).additional
    methods = (tool_class_full[tool_class].objects.get(urlCode = tool_code).method_names)
    server_code = methods['tool'].strip().split('/')[0]
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
    f_name = method_detail.get('function_name')
    if f_name is None or len(f_name) == 0:
        f_name = request.POST['method-code']
    f_name = 'f_' + f_name
    f = importFunction(f'tool.servers.{methods["tool"]}.main', f_name)

    # 不具备复用
    r = f(method_detail)
    return JsonResponse({
        'status': 200,
        'r': True,
        'msg': f'{tool_code} got!',
        'data': r
    })