from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.http.response import Http404
from django.forms import ValidationError
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from UtilGlobal.print import printc
from UtilGlobal.decorator.view_perm import require_login
import json
import random
import os


from account.models import AUser, EmailVerificationCode
from UtilGlobal.email_utils import send_verification_email, generate_verification_code
# Create your views here.



def Home(request):
    return render(request, 'index.html')


def Login(request):
    print('hit login')
    return render(request, 'index.html')


def SignUp(request):
    return render(request, 'index.html')


def SignIn(request):
    return render(request, 'index.html')


def forgetpassword(request):
    return render(request, 'index.html')


@require_POST
def ResetPwd(request):
    print(request.POST)
    form_l = ['username', 'pwd', 'code', 'pwd2']
    try:
        for fl in form_l:
            request.POST[fl]
    except MultiValueDictKeyError:
        raise Http404('wow u got a 404!?-')

    if request.POST['pwd'] == request.POST['pwd2']:
        return HttpResponse(json.dumps({'state': False, 'msg': 4}))

    msg = 0
    state = False
    if request.POST['code'] != request.session['code']:
        msg = 1
    else:
        u = AUser.objects.filter(username = request.POST['username']).first()
        if u and check_password(request.POST['pwd'], u.passwrod):
            state = True
            u = AUser.objects.get(username = request.POST['username'])
            u.password = make_password(request.POST['pwd2'])
            u.save()
        elif u:
            msg = 3
        else:
            msg = 2
        

    '''
    msg choices
    1 验证码错误
    2 没有注册
    3 账号或密码错误
    4 密码一样，放弃修改
    '''
    return HttpResponse(json.dumps({'state': state, 'msg': msg}))


@require_POST
def DoSignIn(request):
    form_l = ['username', 'pwd', 'code']
    # try:
    printc(request.POST, color = [0,255,0])
    for fl in form_l:
        request.POST[fl]
    # except MultiValueDictKeyError:
        # raise Http404('wow u got a 404!?-')
    msg = 0
    state = False
    pwd = request.POST['pwd']
    # pwd = hashlib.sha256((pwd + 'tw').encode('utf-8')).hexdigest()
    if request.session["code"] != request.POST['code'].lower(): # 验证码
        printc('VCODE wrong:', color = [255,47,47])
        printc([f'real:  {request.session["code"]}', f'given: {request.POST["code"]}'], isList = True)
        msg = 1
    else:
        username = request.POST['username']
        u = AUser.objects.filter(username = username).first()
        # if u and check_password(pwd, u.password):
        user = authenticate(request, username = username, password = pwd)
        if u and user is not None:
            state = True
            msg = 11
            # request.session['username'] = username
            login(request, user)
        else:
            msg = 2
            if u:
                printc([pwd, '!=', u.password], isList=True, end = ' ')
            else:
                printc('no such user! (dev message)')
    printc(f'login {"success" if state else "failed"}', color = [255,47,47])
    '''
    msg choices
    1 验证码错误
    2 帐号/密码不正确
    11 成功
    '''
    return HttpResponse(json.dumps({'state': state, 'msg': msg}))


def DoSignUp(request):
    form_l = ['username', 'pwd', 'code', 'invitecode']
    try:
        for fl in form_l:
            request.POST[fl]
    except MultiValueDictKeyError as _:
        raise Http404('wow u got a 404!?')
    printc(request.POST)
    msg = 1
    state = False
    # if checkVcode(request):
    if request.session["code"] != request.POST['code'].lower(): # 验证码
        msg = 1
    else:
        if AUser.objects.filter(username = request.POST.get('username')).exists():
            msg = 3
        elif not settings.DEBUG and request.POST.get('invitecode') != settings.SIGNUP_KEY:
            msg = 4
        else:
            #验证id pwd的规范性（用接口
            pwd = request.POST.get('pwd')
            # pwd = hashlib.sha256((pwd + 'tw').encode('utf-8')).hexdigest()
            
            #设置user的其他field， 用接口
            u = AUser(
                username=request.POST.get('username'),
                password = make_password(pwd),
                additional = {}
            )
            try:
                u.full_clean()
            except ValidationError as e:
                msg = 2
                printc(e)
                return HttpResponse(json.dumps({'state': state, 'msg': msg}))
                return HttpResponseRedirect(reverse('account:sign-up') + '?username=0')
            u.save()
            state = True
            msg = 11
            # request.session['username'] = request.POST['username']
            return HttpResponse(json.dumps({'state': state, 'msg': msg}))
    '''
    msg choices
    1 验证码错误
    2 帐号/密码不合法
    3 该账号已经注册了
    4 需要可用的邀请码
    11 成功
    '''
    return HttpResponse(json.dumps({'state': state, 'msg': msg}))


def getToken(request):
    return HttpResponse(get_token(request))


def isLoggedIn(request):
    if not request.user.is_authenticated:
        return JsonResponse({'r': 0})
    return JsonResponse({'r': 1})


def check_auth(request):
    """Check if user is authenticated for invitation system"""
    logged_in = request.user.is_authenticated
    return JsonResponse({
        'r': 1 if logged_in else 0,
        'logged_in': logged_in
    })


def get_csrf_token(request):
    """Get CSRF token for unauthenticated users"""
    return JsonResponse({
        'csrfToken': get_token(request),
        'r': True
    })


@require_POST
def simple_login(request):
    """Simple login endpoint for invitation system"""
    try:
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        if not username or not password:
            return JsonResponse({'r': 0, 'error': '用户名和密码不能为空'})
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'r': 1, 'success': True})
        else:
            return JsonResponse({'r': 0, 'error': '用户名或密码不正确'})
    except Exception as e:
        return JsonResponse({'r': 0, 'error': '登录时发生错误'})


@require_POST
def send_verification_code(request):
    """Send email verification code"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        
        if not email:
            return JsonResponse({'success': False, 'error': '请输入邮箱地址'})
        
        # Basic email validation
        if '@' not in email or '.' not in email.split('@')[1]:
            return JsonResponse({'success': False, 'error': '请输入有效的邮箱地址'})
        
        # Check if email is already registered
        if AUser.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': '该邮箱已被注册'})
        
        # Generate verification code
        verification_code = generate_verification_code()
        
        try:
            # Save to database with timing restrictions
            EmailVerificationCode.create_code(email, verification_code)
        except ValueError as ve:
            # Timing restriction error
            return JsonResponse({'success': False, 'error': str(ve)})
        
        # Send email
        if send_verification_email(email, verification_code):
            return JsonResponse({'success': True, 'message': '验证码已发送到您的邮箱'})
        else:
            return JsonResponse({'success': False, 'error': '邮件发送失败，请稍后重试'})
            
    except Exception as e:
        print(f"Send verification code error: {e}")
        return JsonResponse({'success': False, 'error': '发送验证码时发生错误'})


@require_POST
def register_with_verification(request):
    """Register user with email verification"""
    try:
        data = json.loads(request.body)
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        nickname = data.get('nickname', '').strip()
        verification_code = data.get('verification_code', '')
        invitation_code = data.get('invitation_code', '').strip()  # Get invitation code
        
        if not all([email, password, nickname, verification_code]):
            return JsonResponse({'success': False, 'error': '请填写所有必填字段'})
        
        # Verify email code
        if not EmailVerificationCode.verify_code(email, verification_code):
            return JsonResponse({'success': False, 'error': '验证码无效或已过期'})
        
        # Check if email is already registered
        if AUser.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': '该邮箱已被注册'})
        
        # Validate password
        if len(password) < 6:
            return JsonResponse({'success': False, 'error': '密码长度至少为6位'})
        
        # Validate invitation code if provided
        invitation = None
        if invitation_code:
            from tool.models import InvitationCode
            try:
                invitation = InvitationCode.objects.get(code=invitation_code)
                if invitation.is_expired:
                    return JsonResponse({'success': False, 'error': '邀请码已过期'})
                if invitation.max_uses > 0 and invitation.remain_uses <= 0:
                    return JsonResponse({'success': False, 'error': '邀请码使用次数已用完'})
            except InvitationCode.DoesNotExist:
                return JsonResponse({'success': False, 'error': '邀请码无效'})
        
        from django.db import transaction
        
        try:
            with transaction.atomic():
                # Create the user
                user = AUser.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=nickname
                )
                
                # If there's a valid invitation, add user to the server
                if invitation:
                    from tool.models import UserServerRole, ServerRole
                    
                    # Check if user is already a member
                    if not UserServerRole.objects.filter(user=user.auser, role__server=invitation.server).exists():
                        # Get the default role (usually "everyone" role)
                        default_role = ServerRole.objects.filter(
                            server=invitation.server,
                            name__iexact="everyone"
                        ).first()
                        
                        if not default_role:
                            # If no "everyone" role, get the first available role
                            default_role = ServerRole.objects.filter(server=invitation.server).first()
                        
                        if default_role:
                            # Create membership through UserServerRole
                            UserServerRole.objects.create(
                                user=user.auser,
                                role=default_role
                            )
                            
                            # Update invitation usage
                            if invitation.max_uses > 0 and invitation.remain_uses > 0:
                                invitation.remain_uses -= 1
                                invitation.save()
                        else:
                            # No role found for server
                            raise ValueError(f"No default role found for server {invitation.server.name}")
                
                # Log the user in
                authenticated_user = authenticate(request, username=email, password=password)
                login(request, authenticated_user)
                
                return JsonResponse({'success': True})
                
        except Exception as e:
            print(f"User creation/server join error: {e}")
            # More specific error handling
            if 'UNIQUE constraint failed' in str(e) or 'already exists' in str(e).lower():
                return JsonResponse({'success': False, 'error': '该邮箱已被注册'})
            elif 'CHECK constraint failed: remain_uses' in str(e):
                return JsonResponse({'success': False, 'error': '邀请链接使用次数已用完'})
            elif 'role' in str(e).lower() or 'server' in str(e).lower():
                return JsonResponse({'success': False, 'error': '加入服务器失败，请稍后重试'})
            else:
                return JsonResponse({'success': False, 'error': '创建账户失败，请稍后重试'})
            
    except Exception as e:
        print(f"Registration error: {e}")
        return JsonResponse({'success': False, 'error': '注册时发生错误'})


def DoLogOut(request):
    if request.session.has_key('username'):
        del request.session['username']
    logout(request)
    return JsonResponse({'r': 1})


def LogOut(request):
    if request.session.has_key('username'):
        del request.session['username']
    logout(request)
    return HttpResponseRedirect(reverse('account:login'))


def Vcode(request):
    width = 90
    height = 35
    size = (width,height)
    #定义背景色
    bg_color = (random.randrange(20,100),random.randrange(20,100),random.randrange(20,100))
    from PIL import Image,ImageDraw,ImageFont
    img = Image.new('RGB',size,bg_color)
    draw = ImageDraw.Draw(img)
    for i in range(100):
        #位置
        point_position = (random.randrange(0,width),random.randrange(0,height))
        #颜色
        point_color = (random.randrange(0,255),255,random.randrange(0,255))
        draw.point(point_position,fill=point_color)
    nums =[]    
    #数字
    for i in range(48,58):
        nums.append(chr(i))
    #小写英文字母
    for i in range(97,123):
        nums.append(chr(i))
    #大写英文字母
    for i in range(65,91):
        nums.append(chr(i))

    code_str = ""
    for i in range(4):
        code_str+=nums[random.randrange(0,len(nums))]
    request.session["code"] = code_str.lower()
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    font_family =  ImageFont.truetype(os.path.join(BASE_DIR, 'static') + '/wss/Chalkboard.ttc',25)   
    font_color=(255,random.randrange(0,255),random.randrange(0,255))
    draw.text((5,0),text=code_str[0],font=font_family,fill=font_color)
    draw.text((width/4,0),text=code_str[1],font=font_family,fill=font_color)
    draw.text((width/2,0),text=code_str[2],font=font_family,fill=font_color)
    draw.text((width*3/4,0),text=code_str[3],font=font_family,fill=font_color)
    del draw
    import io
    buf = io.BytesIO()
    img.save(buf,'png')
    return HttpResponse(buf.getvalue(),'image/png')


def avatar_view(request, user_code):
    user = get_object_or_404(AUser, urlCode=user_code)
    if user.avatar:
        return FileResponse(user.avatar.open(), content_type='image/jpeg')
    else:
        # Handle the case where the user does not have an avatar
        pass


@require_login
def getOwnInfo(request):
    u = request.user
    res = {
        'username': u.username,
        'avatar': '' if u.auser.avatar is None or u.auser.avatar.name == '' else u.auser.avatar.url
    }
    return JsonResponse(res)