from django.shortcuts import render
from django.middleware.csrf import get_token
from django.http import HttpResponse
# Create your views here.


def Home(request):
    return render(request, 'user/index.html')


def Login(request):
    return render(request, 'user/index.html')


def Signup(request):
    return render(request, 'user/index.html')


def getToken(request):
    return HttpResponse(get_token(request))