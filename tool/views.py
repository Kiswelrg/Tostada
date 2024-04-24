from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import ToolServer, Tool, UserServerRole, UserToolRole, ToolOfInputAndOutput, ToolOfChat
from UtilGlobal.print import printc
from .util.ImportTool import import_function_from_file, importFunction
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


# Fetch a specific tool server by its urlCode
def fetch_tool_server(request, tool_server_code):
    tool_server = get_object_or_404(ToolServer, urlCode=tool_server_code)
    tools = None
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
        # If already a member of the server, (assume got all reading access to ths tools inside)
        tools = Tool.objects.filter(server=tool_server)
    else:
        tool_ids = UserToolRole.objects.filter(
        user__username=request.session['username'],
        tool__server=tool_server
        ).values_list('tool', flat=True)

        # Get the corresponding tool objects
        if tool_ids.exists():
            tools = Tool.objects.filter(id__in=tool_ids)
    
    category_dict = {}
    for tool in tools:
        t = {
                "cid": str(tool.urlCode),
                "name": tool.name,
                "description": tool.description,
                "category": {
                    'type': tool.category.get_type_display()
                }
            }
        if tool.category.name not in category_dict:
            category_dict[tool.category.name] = [t]
        else:
            category_dict[tool.category.name].append(t)
    print(category_dict)
    if tools:
        data["category"] = category_dict
    else:
        print('no joined server/available tool')
    return JsonResponse({"tool_server": data, "r": True, "type": "with-tool"})


# Fetch a specific tool by its urlCode
def fetch_tool(request, tool_code):
    tool = get_object_or_404(Tool, urlCode=tool_code)
    # user_tool = None

    if not UserServerRole.objects.filter(server=tool.server, user__username=request.session['username']).exists():
        if not UserToolRole.objects.filter(user__username=request.session['username'], tool=tool).exists():
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
    }
    if 'subclass' not in tool.additional:
        pass
    elif tool.additional['subclass'] == 'ToolOfInputAndOutput':
        from .models import ToolOfInputAndOutput
        tool_specific = get_object_or_404(ToolOfInputAndOutput, id = tool.id)
        data['methods'] = tool_specific.method_names
    elif tool.additional['subclass'] == 'ToolOfChat':
        pass
    return JsonResponse({"tool": data, "r": True})


subtools = {
    'ToolOfInputAndOutput': ToolOfInputAndOutput,
    'ToolOfChat': ToolOfChat
}
@require_POST
def run_tool(request, tool_code):
    printc([request.POST, tool_code], isList=True, color=[255,255,0])
    add = Tool.objects.get(urlCode = tool_code).additional
    methods = (subtools[add['subclass']].objects.get(urlCode = tool_code).method_names)
    server_code = methods['tool'].strip().split('/')[0]
    method_detail = None
    for g in methods['groups']:
        for m in g['methods']:
            if m['code'] == int(request.POST['method-code']):
                method_detail = m
                break
        if method_detail:
            break
    
    
    f = importFunction(f'tool.servers.{methods["tool"]}.main', 'f_' + request.POST['method-code'])
    return JsonResponse({
        'status': 200,
        'r': True,
        'msg': f'{tool_code} got!'
    })