from django.urls import path, re_path
from . import views

app_name = 'message'
urlpatterns = [
    # Room management
    path('rooms/', views.list_rooms, name='list-rooms'),
    path('rooms/', views.create_room, name='create-room'),  # POST
    re_path(r'^rooms/(?P<cid>\d+)/$', views.get_room_details, name='room-details'),
    
    # Messages
    re_path(r'^rooms/(?P<cid>\d+)/messages/$', views.get_room_messages, name='room-messages'),
    re_path(r'^rooms/(?P<cid>\d+)/mark_read/$', views.mark_messages_read, name='mark-read'),
    re_path(r'^rooms/(?P<cid>\d+)/history/$', views.get_message_history, name='message-history'),
    
    # Search
    path('search/', views.search_messages, name='search-messages'),
]