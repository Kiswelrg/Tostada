from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from .models import ToolServer, Tool, UserServerRole, UserToolRole
# Create your views here.
def Home(request):
    return render(request, 'index.html')


# Fetch all tool servers that a user has joined
def fetch_user_tool_servers(request):
    tool_servers = ToolServer.objects.filter(user_server_auths__user__username=request.session['username'])
    data = [
        {
            "cid": ts.urlCode,
            "name": ts.name,
            "description": ts.description,
            "logoSrc": '/media/default/server/logo/logo.svg' if ts.logo == '' else ts.logo.url
        } for ts in tool_servers
    ]
    return JsonResponse({"tool_servers": data, 'r': 'success'})


# Fetch a specific tool server by its urlCode
def fetch_tool_server(request, tool_server_code):
    tool_server = get_object_or_404(ToolServer, urlCode=tool_server_code)
    tools = None
    data = {
        "cid": tool_server.urlCode,
        "name": tool_server.name,
        "description": tool_server.description,
        "status": tool_server.get_status_display(),
        "type": tool_server.get_type_display(),
        "date_created": tool_server.date_created.date(),
    }

    if 'tools' not in request.GET or not request.GET['tools'] == '1':
        return JsonResponse({"tool_server": data})
    
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
                "cid": tool.urlCode,
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
    return JsonResponse({"tool_server": data})


# Fetch a specific tool by its urlCode
def fetch_tool(request, tool_code):
    tool = get_object_or_404(Tool, urlCode=tool_code)
    user_tool = None
    try:
        tool_id = UserToolRole.objects.filter(user__username=request.session['username']).values_list('tool', flat=True)[0]
        user_tool = Tool.objects.get(id = tool_id)
    except UserToolRole.DoesNotExist:
        if not UserServerRole.objects.filter(server=tool.server, user__username=request.session['username']).exists():
            return JsonResponse({})
        user_tool = tool
    
    data = {
        "cid": user_tool.urlCode,
        "name": user_tool.name,
        "description": user_tool.description,
        "status": user_tool.get_status_display(),
        "date_created": user_tool.date_created.date(),
        "server": user_tool.server.name,
        "category": user_tool.category.name,
    }
    return JsonResponse({"tool": data, "r": "success"})
