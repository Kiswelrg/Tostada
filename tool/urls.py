from django.urls import path, re_path
from . import views

# return HttpResponseRedirect(reverse('user:sign-up') + '?username=0')

app_name = 'tool'
urlpatterns = [

	# re_path(r'^search/(?:(?P<page>[0-9]{1,3})(?:[&=\w]+)/)?$',views.Search, name = 'search'),
	path('', views.Home, name='slash'),
	path('user/<int:user_code>/tool_servers/', views.fetch_user_tool_servers, name='fetch_user_tool_servers'),
    path('tool_server/<int:tool_server_code>/', views.fetch_tool_server, name='fetch_tool_server'),
    path('tool/<int:tool_code>/', views.fetch_tool, name='fetch_tool'),
	re_path(r'.*',views.Home, name = 'home'),
]