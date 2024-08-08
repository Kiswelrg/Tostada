from django.urls import path, re_path
from . import views

app_name = 'attachment'
urlpatterns = [
    re_path(r'^(?P<channel_cid>\d{17,19})/(?P<attachment_cid>\d{17,19})/(?P<attachment_name>[\w\.]{1,256})$', views.msg_attachment, name='msg_attachment'),
    
	# re_path(r'^(?:login/)?$',views.Login, name = 'login'),
	# path('signup/', views.SignUp, name = 'sign-up'),
	# path('',views.Home, name = 'home'),
	
]