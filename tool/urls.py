from django.urls import path, re_path
from . import views

# return HttpResponseRedirect(reverse('user:sign-up') + '?username=0')

app_name = 'tool'
urlpatterns = [

	# re_path(r'^search/(?:(?P<page>[0-9]{1,3})(?:[&=\w]+)/)?$',views.Search, name = 'search'),
	re_path(r'.*',views.Home, name = 'home'),
	
]