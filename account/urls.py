from django.urls import path, re_path
from . import views

# return HttpResponseRedirect(reverse('account:sign-up') + '?username=0')

app_name = 'account'
urlpatterns = [
    re_path(r'^avatar/(?P<user_code>\d{1,9})/$', views.avatar_view, name='user_avatar'),
    
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
	path('check-auth/',views.check_auth, name = 'check-auth'),
	path('get-csrf-token/',views.get_csrf_token, name = 'get-csrf-token'),
	path('login/',views.simple_login, name = 'simple-login'),
	path('send-verification-code/',views.send_verification_code, name = 'send-verification-code'),
	path('register-with-verification/',views.register_with_verification, name = 'register-with-verification'),
	path('Vcode/',views.Vcode, name = 'Vcode'),
	path('info/',views.getOwnInfo, name = 'own-info'),
	# re_path(r'^search/(?:(?P<page>[0-9]{1,3})(?:[&=\w]+)/)?$',views.Search, name = 'search'),
	path('',views.Home, name = 'home'),
	
]