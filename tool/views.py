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
from django.utils import timezone
from .models import InvitationCode


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
    data = {}
    for us in u_s_role:
        cur_code = us.role.server.urlCode
        if cur_code in data:
            continue
        data[cur_code] = {
            "cid": str(us.role.server.urlCode),
            "name": us.role.server.name,
            "description": us.role.server.description,
            "logoSrc": '/media/default/server/logo/logo.svg' if us.role.server.logo == '' else us.role.server.logo.url,
            "order": us.order,
            "date_added": us.date_added.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
    
    return JsonResponse({"tool_servers": [v for k,v in data.items()], 'r': True})


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
        if u_s_r.order != 0 and u_s_r.order != change_list[u_s_r.role.server.urlCode]['old_order']:
            raise Http404('Malicious Server Reorder')
        u_s_r.order = change_list[u_s_r.role.server.urlCode]['order']
        u_s_r.full_clean()
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
        if c_in_s.order != 0 and c_in_s.order != change_list[c_in_s.urlCode]['old_order']:
            raise Http404('Malicious Category Reorder')
        c_in_s.order = change_list[c_in_s.urlCode]['order']
        c_in_s.full_clean()
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
    if tool.additional is None or Sub_Tool.__name__ == 'ChannelOfChat':
        # if no additional is presented, just treat it like ChannelOfChat
        tool_specific = get_object_or_404(ChannelOfChat, pk = tool.pk).tools.all()
        data['methods'] = {
            "groups": [
                {
                    "methods": [
                        {
                            "display_name": tool.display_name,
                            "cid": tool.urlCode,
                            "input": tool.params['main'],
                            "output": tool.res['main']
                        } for tool in tool_specific
                    ]
                }
            ]
        }
    elif 'sub_class' not in tool.additional:
        pass
    elif Sub_Tool.__name__ == 'ChannelOfVoice':
        pass


    return JsonResponse({"tool": data, "r": True})


def getMethodsFromTool(c):
    return {
        "groups": [
            {
                'methods': [
                    {
                        'display_name': tool.display_name,
                        'function_name': tool.function_name,
                        'cid': tool.urlCode,
                        'data': tool.data
                    } for tool in c.tools.all()
                ]
            }
        ]
    }



def fetch_TOOL_SECRET_KEY(user_cid):
    return "1"


@require_POST
@require_login
def run_tool(request, channel_cid):
    """
    here tool means Channel
    """
    printc([request.POST, channel_cid], isList=True, color=[255,255,0])
    tool_class = request.POST['sub_class']
    tool_model = tool_class_full[tool_class]
    channel = tool_model.objects.filter(urlCode=channel_cid)
    u = request.user.auser
    if not channel.exists():
        raise PermissionDenied
    else:
        channel = channel[0]
        roles = ServerRole.objects.filter(user_server_auths__user=u, server=channel.server)
        if not roles.exists():
            raise PermissionDenied
        hasAuth = False
        for r in roles:
            v = r.auth_value
            if (v & AuthBits['Manage Channels'] > 0) or (v & AuthBits['Administrator'] > 0):
                hasAuth = True
                break
        if not hasAuth: raise PermissionDenied


    methods = getMethodsFromTool(tool_model.objects.get(urlCode = channel_cid))
    method_detail = None
    for g in methods['groups']:
        for m in g['methods']:
            if m['cid'] == int(request.POST['method-cid']):
                method_detail = m
                break
        if method_detail:
            break
    if method_detail is None:
        raise Http404()
    name = method_detail.get('function_name')
    if name is None or len(name) == 0:
        name = request.POST['method-cid']
    f_name = 'f_' + name
    f = importFunction(f'tool.servers.{channel.server.urlCode}.{channel_cid}.main', f_name)

    # 不具备复用
    from .util.toolAPI import generate_temp_link
    method_detail['inputs'] = dict(request.POST)
    r = f(method_detail, u, channel_cid, TOOL_SECRET_KEY=fetch_TOOL_SECRET_KEY(u.urlCode), generate_link_func=generate_temp_link)
    return JsonResponse({
        'status': 200,
        'r': True,
        'msg': f'{channel_cid} got!',
        'data': r
    })



def tool_api(requests, user_cid, tool_cid, token):
    TOOL_SECRET_KEY = fetch_TOOL_SECRET_KEY(user_cid)
    if TOOL_SECRET_KEY == "":
        raise PermissionDenied

    from .util.toolAPI import verify_and_process_temp_link
    from .util.toolAPI import generate_temp_link
    return HttpResponse(verify_and_process_temp_link(user_cid, tool_cid, token, TOOL_SECRET_KEY, generate_link_func=generate_temp_link), content_type="text/plain; charset=utf-8")

# Invitation views
@require_login
@require_POST
def create_invitation(request, server_id):
    """
    Create a new invitation code for a server.
    
    POST Parameters:
        duration_minutes: Duration in minutes the invitation will be valid, 0 means never expires
        max_uses: Maximum number of times the invitation can be used, 0 means unlimited
    """
    try:
        server = get_object_or_404(Server, urlCode=server_id)
        duration_minutes = int(request.POST.get('duration_minutes', 10080))  # Default 7 days
        max_uses = int(request.POST.get('max_uses', 0))  # Default unlimited uses
        
        # Check if an invitation with the same settings already exists for this user
        existing_invitations = InvitationCode.objects.filter(
            server=server,
            user_created=request.user.auser,
            valid_duration_minutes=duration_minutes,
            max_uses=max_uses
        )
        
        # Filter out expired invitations and delete them
        valid_existing = []
        expired_invitations = []
        for inv in existing_invitations:
            if inv.is_expired or (inv.max_uses > 0 and inv.remain_uses <= 0):
                expired_invitations.append(inv)
            else:
                valid_existing.append(inv)
        
        # Delete expired/used up invitations from database
        if expired_invitations:
            for inv in expired_invitations:
                inv.delete()
        
        # If a valid invitation with the same settings exists, return it
        if valid_existing:
            invitation = valid_existing[0]
        else:
            # Create a new invitation if none exists with these settings
            invitation = InvitationCode.create_invitation(
                server=server,
                user=request.user.auser,
                duration_minutes=duration_minutes,
                max_uses=max_uses
            )
        
        # Return invitation details
        expiry_time = invitation.expiry_time.strftime("%Y-%m-%dT%H:%M:%SZ") if invitation.expiry_time else "Never"
        return JsonResponse({
            'code': invitation.code,
            'max_uses': invitation.max_uses,
            'max_uses_display': "∞" if invitation.max_uses == 0 else str(invitation.max_uses),
            'remain_uses': invitation.remain_uses,
            'remain_uses_display': "∞" if invitation.remain_uses == 0 else str(invitation.remain_uses),
            'valid_until': expiry_time,
            'is_permanent': invitation.is_permanent,
            'r': True
        })
    except PermissionError as e:
        return JsonResponse({'error': str(e), 'r': False}, status=403)
    except Exception as e:
        return JsonResponse({'error': 'An error occurred', 'r': False}, status=500)


@require_POST
@require_login
def use_invitation(request, invitation_code):
    """
    Use an invitation code to join a server.
    """
    try:
        # Find the invitation code
        invitation = get_object_or_404(InvitationCode, code=invitation_code)
        
        # Check if invitation is expired
        if invitation.is_expired:
            return JsonResponse({'error': 'Invitation code has expired', 'r': False}, status=400)
        
        # Check if user is already a member of the server
        user = request.user.auser
        if UserServerRole.objects.filter(user=user, role__server=invitation.server).exists():
            return JsonResponse({'error': 'You are already a member of this server', 'r': False}, status=400)
        
        # Add user to the server with the default role
        # Try to find 'everyone' role first, then fall back to any available role
        default_role = ServerRole.objects.filter(server=invitation.server).first()
        if not default_role:
            return JsonResponse({'error': 'Server has no available roles', 'r': False}, status=500)
        
        UserServerRole.objects.create(
            user=user,
            role=default_role
        )
        
        # Decrease remain_uses if it's not unlimited (0)
        if invitation.remain_uses > 0:
            invitation.remain_uses -= 1
            invitation.save()
        
        # Return success
        return JsonResponse({
            'server': {
                'cid': str(invitation.server.urlCode),
                'name': invitation.server.name,
                'description': invitation.server.description,
                'logoSrc': '/media/default/server/logo/logo.svg' if invitation.server.logo == '' else invitation.server.logo.url,
            },
            'r': True
        })
    except Exception as e:
        print(f"Use invitation error: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({'error': f'An error occurred: {str(e)}', 'r': False}, status=500)

@require_login
def get_server_invitations(request, server_id):
    """
    Get all active invitations for a server.
    """
    try:
        server = get_object_or_404(Server, urlCode=server_id)
        
        # Check if user has permission to view invitations
        user = request.user.auser
        user_roles = UserServerRole.objects.filter(user=user, role__server=server)
        
        if not user_roles.exists() and server.owner != user:
            return JsonResponse({'error': 'You do not have permission to view invitations for this server', 'r': False}, status=403)
        
        # Get all active invitations - handle both limited and unlimited invitations
        invitations = InvitationCode.objects.filter(server=server).order_by('-created_at')
        
        # Filter out expired invitations and delete them
        active_invitations = []
        expired_invitations = []
        for inv in invitations:
            if inv.is_expired or (inv.max_uses > 0 and inv.remain_uses <= 0):
                expired_invitations.append(inv)
            else:
                active_invitations.append(inv)
        
        # Delete expired/used up invitations from database
        if expired_invitations:
            for inv in expired_invitations:
                inv.delete()
        
        # Sort invitations by priority: 
        # 1. Permanent invitations (unlimited uses, never expires)
        # 2. Unlimited uses
        # 3. Longer expiry times
        # 4. Higher max uses
        # 5. Most recently created
        def invitation_priority(inv):
            # Permanent invitations come first
            if inv.is_permanent:
                return (0, 0, 0, inv.created_at.timestamp())
            
            # Then consider unlimited uses
            uses_factor = 0 if inv.max_uses == 0 else 1
            
            # Then consider expiry time (never expires trumps all)
            if inv.valid_duration_minutes == 0:
                duration_factor = 0
            else:
                # Longer durations are better (negative for sorting)
                duration_factor = -inv.valid_duration_minutes
            
            # Then max uses (higher is better, negative for sorting)
            max_uses = -inv.max_uses if inv.max_uses > 0 else 0
            
            # Finally, creation time (newer is better)
            created_at = -inv.created_at.timestamp()
            
            return (uses_factor, duration_factor, max_uses, created_at)
            
        active_invitations.sort(key=invitation_priority)
        
        # Return invitations
        return JsonResponse({
            'invitations': [
                {
                    'code': inv.code,
                    'created_by': inv.user_created.username,
                    'created_at': inv.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    'expires_at': inv.expiry_time.strftime("%Y-%m-%dT%H:%M:%SZ") if inv.expiry_time else "Never",
                    'max_uses': inv.max_uses,
                    'max_uses_display': "∞" if inv.max_uses == 0 else str(inv.max_uses),
                    'remain_uses': inv.remain_uses,
                    'remain_uses_display': "∞" if inv.remain_uses == 0 else str(inv.remain_uses),
                    'is_permanent': inv.is_permanent,
                    'valid_duration_minutes': inv.valid_duration_minutes
                } for inv in active_invitations
            ],
            'r': True
        })
    except Exception as e:
        return JsonResponse({'error': 'An error occurred', 'r': False}, status=500)


def check_invitation(request, invitation_code):
    """
    Check if an invitation code is valid without using it.
    """
    try:
        # Find the invitation code
        invitation = get_object_or_404(InvitationCode, code=invitation_code)
        
        # Check if invitation is expired
        if invitation.is_expired:
            return JsonResponse({
                'valid': False, 
                'error': 'Invitation code has expired', 
                'r': False
            })
        
        # Check if invitation has no remaining uses
        if invitation.max_uses > 0 and invitation.remain_uses <= 0:
            return JsonResponse({
                'valid': False, 
                'error': 'Invitation code has no remaining uses', 
                'r': False
            })
        
        # Check if user is already a member of the server (only if logged in)
        if request.user.is_authenticated:
            user = request.user.auser
            if UserServerRole.objects.filter(user=user, role__server=invitation.server).exists():
                return JsonResponse({
                    'valid': False,
                    'error': 'You are already a member of this server', 
                    'r': False
                })
        
        # Return server information if the invitation is valid
        return JsonResponse({
            'valid': True,
            'server': {
                'cid': str(invitation.server.urlCode),
                'name': invitation.server.name,
                'description': invitation.server.description,
                'logoSrc': '/media/default/server/logo/logo.svg' if invitation.server.logo == '' else invitation.server.logo.url,
            },
            'invitation': {
                'code': invitation.code,
                'created_by': invitation.user_created.username,
                'created_at': invitation.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                'expires_at': invitation.expiry_time.strftime("%Y-%m-%dT%H:%M:%SZ") if invitation.expiry_time else "Never",
                'max_uses': invitation.max_uses,
                'max_uses_display': "∞" if invitation.max_uses == 0 else str(invitation.max_uses),
                'remain_uses': invitation.remain_uses,
                'remain_uses_display': "∞" if invitation.remain_uses == 0 else str(invitation.remain_uses),
                'is_permanent': invitation.is_permanent
            },
            'r': True
        })
    except Exception as e:
        return JsonResponse({'valid': False, 'error': 'An error occurred', 'r': False}, status=500)