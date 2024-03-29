from django.urls import path, re_path
from . import views

# return HttpResponseRedirect(reverse('user:sign-up') + '?username=0')

app_name = 'account'
urlpatterns = [
    re_path(r'^avatar/(?P<user_code>(10\d)\d{7})/$', views.avatar_view, name='user_avatar'),
    
	re_path(r'^(?:login/)?$',views.Login, name = 'login'),
	# path('clearUserId/', views.clearStuId, name = 'clear-user-id'),
	path('signup/', views.SignUp, name = 'sign-up'),
    path('dosignup/', views.DoSignUp, name = 'do-sign-up'),
	path('signin/', views.SignIn, name = 'sign-in'),
	path('dosignin/', views.DoSignIn, name = 'do-sign-in'),
	path('logout/', views.LogOut, name = 'log-out'),
	path('dologout/', views.DoLogOut, name = 'do-log-out'),
	path('forgetpassword/',views.forgetpassword, name = 'forget-pwd'),
	path('resetpwd/',views.ResetPwd, name = 'reset-pwd'),
	path('Token/',views.getToken),
	path('isLoggedIn/',views.isLoggedIn, name = 'is-logged-in'),
	path('Vcode/',views.Vcode, name = 'Vcode'),
	# re_path(r'^search/(?:(?P<page>[0-9]{1,3})(?:[&=\w]+)/)?$',views.Search, name = 'search'),
	path('',views.Home, name = 'home'),
	
]