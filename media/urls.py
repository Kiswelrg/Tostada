from django.urls import path, re_path
from . import views

app_name = 'media'
urlpatterns = [
    # Server
    re_path(r'^logo/(?P<server_cid>\d{1,19})/(?P<logo_name>[\w\-.%]{1,500})$', views.logo, name='logo'),
    re_path(r'^cover/(?P<server_cid>\d{1,19})/(?P<cover_name>[\w\-.%]{1,500})$', views.cover, name='cover'),
    # AUser
	re_path(r'^avatar/(?P<user_cid>\d{1,19})/(?P<avatar_name>[\w\-.%]{1,500})$', views.avatar, name='avatar'),
	re_path(r'^usercover/(?P<user_cid>\d{1,19})/(?P<usercover_name>[\w\-.%]{1,500})$', views.usercover, name='usercover'),
    
	# re_path(r'^(?:login/)?$',views.Login, name = 'login'),
	# path('signup/', views.SignUp, name = 'sign-up'),
	# path('',views.Home, name = 'home'),
	
]