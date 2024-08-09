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
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from UtilGlobal.print import printc
import hashlib
import json
import random
import os


from account.models import AUser
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

    printc(request.POST)
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
            request.session['isLoggedIn'] = True
            request.session['username'] = username
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
        elif request.POST.get('invitecode') != settings.SIGNUP_KEY:
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
                u.clean_fields()
            except ValidationError as e:
                msg = 2
                printc(e)
                return HttpResponse(json.dumps({'state': state, 'msg': msg}))
                return HttpResponseRedirect(reverse('account:sign-up') + '?username=0')
            u.save()
            state = True
            msg = 11
            request.session['isLoggedIn'] = True
            request.session['username'] = request.POST['username']
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
    if not request.session.has_key('isLoggedIn') or not request.session.has_key('username') or not request.session['isLoggedIn']:
        return JsonResponse({'r': 0})
    return JsonResponse({'r': 1})


def DoLogOut(request):
    if request.session.has_key('isLoggedIn'):
        del request.session['isLoggedIn']
    if request.session.has_key('username'):
        del request.session['username']
    logout(request)
    return JsonResponse({'r': 1})


def LogOut(request):
    if request.session.has_key('isLoggedIn'):
        del request.session['isLoggedIn']
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