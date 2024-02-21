from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.http.response import Http404
from django.forms import ValidationError
from django.http.response import HttpResponseRedirect
from django.urls import reverse
import hashlib
from user.models import User

from django.conf import settings
import json
import random
import os
# Create your views here.

def printc(info, isList = False, color = None):
    def printRGB(text):
        def rgb_to_ansi(r, g, b):
            # Convert RGB values to a color index
            index = 16 + (36 * round(r * 5 / 255)) + (6 * round(g * 5 / 255)) + round(b * 5 / 255)
            # Return the ANSI escape sequence
            return f"\033[38;5;{index}m"
        if color:
            # Convert RGB to ANSI color code
            ansi_code = rgb_to_ansi(color[0], color[1], color[2])
            print(f"{ansi_code}{text}\033[0m")
        else:
            print(text)
    if settings.VERBOSE:
        if isList:
            for i in info:
                printRGB(i)
            return
        printRGB(info)

def Home(request):
    return render(request, 'index.html')


def Login(request):
    return render(request, 'index.html')


def SignUp(request):
    return render(request, 'index.html')


def SignIn(request):
    return render(request, 'index.html')


def forgetpassword(request):
    return render(request, 'index.html')


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
    elif not User.objects.filter(username = request.POST['username']).exists():
        msg = 2
    elif not User.objects.filter(username = request.POST['username'], password = hashlib.sha256((request.POST['pwd'] + 'tw').encode('utf-8')).hexdigest()).exists():
        msg = 3
    else:
        state = True
        pwd2 = hashlib.sha256((request.POST['pwd2'] + 'tw').encode('utf-8')).hexdigest()
        u = User.objects.get(username = request.POST['username'])
        u.password = pwd2
        u.save()

    '''
    msg choices
    1 验证码错误
    2 没有注册
    3 账号或密码错误
    4 密码一样，放弃修改
    '''
    return HttpResponse(json.dumps({'state': state, 'msg': msg}))


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
    pwd = hashlib.sha256((pwd + 'tw').encode('utf-8')).hexdigest()
    if request.session["code"] != request.POST['code'].lower(): # 验证码
        printc('VCODE wrong:', color = [255,47,47])
        printc([f'real:  {request.session["code"]}', f'given: {request.POST["code"]}'], isList = True)
        msg = 1
    elif User.objects.filter(username = request.POST['username'], password = pwd):
        state = True
        msg = 11
        request.session['isLoggedIn'] = True
        request.session['username'] = request.POST['username']
    else:
        msg = 2
        printc([request.POST['pwd'], pwd], isList=True)
    printc(f'login {"success" if state else "failed"}', color = [255,47,47])
    '''
    msg choices
    1 验证码错误
    2 帐号/密码不正确
    11 成功
    '''
    return HttpResponse(json.dumps({'state': state, 'msg': msg}))


def DoSignUp(request):
    form_l = ['username', 'pwd', 'code']
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
        if User.objects.filter(username = request.POST.get('username')).exists():
            msg = 3
        else:
            #验证id pwd的规范性（用接口
            pwd = request.POST.get('pwd')
            # pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
            pwd = hashlib.sha256((pwd + 'tw').encode('utf-8')).hexdigest()
            
            #设置user的其他field， 用接口
            u = User(
                username=request.POST.get('username'),
                password = pwd,
                additional = {}
            )
            try:
                u.clean_fields()
            except ValidationError as e:
                msg = 2
                printc(e)
                return HttpResponse(json.dumps({'state': state, 'msg': msg}))
                return HttpResponseRedirect(reverse('user:sign-up') + '?username=0')
            u.save()
            state = True
            msg = 11
            return HttpResponse(json.dumps({'state': state, 'msg': msg}))
    '''
    msg choices
    1 验证码错误
    2 帐号/密码不合法
    3 该账号已经注册了
    11 成功
    '''
    return HttpResponse(json.dumps({'state': state, 'msg': msg}))


def getToken(request):
    return HttpResponse(get_token(request))

def DoLogOut(request):
    if request.session.has_key('isLoggedIn'):
        del request.session['isLoggedIn']
    if request.session.has_key('username'):
        del request.session['username']
    return HttpResponseRedirect('/')


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