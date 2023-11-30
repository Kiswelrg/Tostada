from django.shortcuts import render

# Create your views here.


def Home(request):
    return render(request, 'user/index.html')


def Login(request):
    return render(request, 'user/index.html')


def Signup(request):
    return render(request, 'user/index.html')