from django.urls import path, re_path
from . import views

# return HttpResponseRedirect(reverse('user:sign-up') + '?username=0')

app_name = 'user'
urlpatterns = [
	re_path(r'^(?:login/)?$',views.Login, name = 'login'),
	# path('clearUserId/', views.clearStuId, name = 'clear-user-id'),
	# path('signup/', views.signup, name = 'sign-up'),
	path('signup/', views.Signup, name = 'sign-up'),
	# path('signIn/', views.signIn, name = 'sign-In'),
	# path('signin/', views.signin, name = 'sign-in'),
	# path('forgetpassword/',views.forgetpassword, name = 'forget-pwd'),
	# path('resetPwd/',views.resetPwd, name = 'reset-pwd'),
	# path('Token/',views.getToken),
	# path('getUsername/',views.getUsername),
	# path('Vcode/',views.Vcode, name = 'Vcode'),
	# re_path(r'^search/(?:(?P<page>[0-9]{1,3})(?:[&=\w]+)/)?$',views.Search, name = 'search'),
	re_path(r'.*',views.Home, name = 'home'),
	
]