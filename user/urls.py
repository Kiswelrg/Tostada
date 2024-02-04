from django.urls import path, re_path
from . import views

# return HttpResponseRedirect(reverse('user:sign-up') + '?username=0')

app_name = 'user'
urlpatterns = [
	re_path(r'^(?:login/)?$',views.Login, name = 'login'),
	# path('clearUserId/', views.clearStuId, name = 'clear-user-id'),
	path('signup/', views.SignUp, name = 'sign-up'),
    path('dosignup/', views.DoSignUp, name = 'do-sign-up'),
	path('signin/', views.SignIn, name = 'sign-in'),
	path('dosignin/', views.DoSignIn, name = 'do-sign-in'),
	path('forgetpassword/',views.forgetpassword, name = 'forget-pwd'),
	path('resetpwd/',views.ResetPwd, name = 'reset-pwd'),
	path('Token/',views.getToken),
	# path('getUsername/',views.getUsername),
	path('Vcode/',views.Vcode, name = 'Vcode'),
	# re_path(r'^search/(?:(?P<page>[0-9]{1,3})(?:[&=\w]+)/)?$',views.Search, name = 'search'),
	re_path(r'.*',views.Home, name = 'home'),
	
]