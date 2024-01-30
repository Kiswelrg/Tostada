from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.http.response import Http404
from django.forms import ValidationError
from django.http.response import HttpResponseRedirect
from django.urls import reverse
import hashlib


import random
import os
# Create your views here.


def Home(request):
    return render(request, 'user/index.html')


def Login(request):
    return render(request, 'user/index.html')


def SignUp(request):
    return render(request, 'user/index.html')


def DoSignUp(request):
    form_l = ['username', 'pwd', 'code']
    try:
        for fl in form_l:
            request.POST[fl]
    except MultiValueDictKeyError:
        raise Http404('wow u got a 404!?')
    print(request.POST)
    msg = 1
    state = False
    # 这里验证码 + ifinouc
    # if checkVcode(request):
    if request.session["code"] != request.POST['code'].lower(): # 验证码
        msg = 1
    elif request.session.has_key("stu_id") and request.session["stu_id"]:
        if User.objects.filter(stu_id = request.session["stu_id"]).exists():
            msg = 2
        elif User.objects.filter(username = request.POST.get('username')).exists():
            msg = 3
        else:
            #验证id pwd的规范性（用接口

            pwd = request.POST.get('pwd')
            pwd = hashlib.sha256(pwd.encode('utf-8')).hexdigest()
            pwd = hashlib.sha256((pwd + 'ouc').encode('utf-8')).hexdigest()
            
            #设置user的其他field， 用接口
            u = User(
                stu_id=int(request.session["stu_id"]),
                username=request.POST.get('username'),
                password = pwd
            )
            try:
                u.clean_fields()
            except ValidationError:
                print(1)
                return HttpResponseRedirect(reverse('user:sign-up') + '?username=0')
            u.save()
            state = True
            del request.session["stu_id"]
    else:
        raise Http404('wow u got a 404!?')
    
    '''
    msg choices
    1 验证码错误
    2 该学号已经注册了
    3 该账号已经注册了
    '''
    return HttpResponse(json.dumps({'state': state, 'msg': msg}))


def getToken(request):
    return HttpResponse(get_token(request))



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