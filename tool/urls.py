from django.urls import path, re_path
from . import views

# return HttpResponseRedirect(reverse('account:sign-up') + '?username=0')

app_name = 'tool'
urlpatterns = [

	# re_path(r'^search/(?:(?P<page>[0-9]{1,3})(?:[&=\w]+)/)?$',views.Search, name = 'search'),
	path('', views.Home, name='slash'),
	path('user/tool_servers/', views.fetch_user_tool_servers, name='fetch_user_tool_servers'),
    path('tool_server/<int:tool_server_code>/', views.fetch_tool_server, name='fetch_tool_server'),
    path('tool/<str:tool_class>/<int:tool_code>/', views.fetch_tool, name='fetch_tool'),
    re_path(r'^runtool/(?P<channel_cid>[0-9]{1,19})/$', views.run_tool, name='run_tool'),
    path('toolapi/<int:user_cid>/<int:tool_cid>/<str:token>/', views.tool_api, name='tool_api'),
    path('reorderss/', views.reorderServers, name='reorder_server'),
    path('reordersc/', views.reorderServerCategorys, name='reorder_category'),
	# re_path(r'',views.Home, name = 'home'),
    
    # Invitation URLs
    path('server/<int:server_id>/invitations/', views.get_server_invitations, name='get_server_invitations'),
    path('server/<int:server_id>/create_invitation/', views.create_invitation, name='create_invitation'),
    path('invitation/<str:invitation_code>/use/', views.use_invitation, name='use_invitation'),
    path('invitation/<str:invitation_code>/check/', views.check_invitation, name='check_invitation'),
]