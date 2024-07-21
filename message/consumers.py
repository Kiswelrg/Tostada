import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.utils import timezone
from .models import GroupMessage
from tool.models import ChannelOfChat
from account.models import AUser
from .Storage.chat import RedisChatStorage
if settings.PRODUCTION:
    ChatStorage = RedisChatStorage
else:
    ChatStorage = RedisChatStorage


def require_login(consumer_func):
    async def wrapper(self, *args, **kwargs):
        if not await self.check_authentication():
            await self.close()
            return
        return await consumer_func(self, *args, **kwargs)
    return wrapper

class ChatConsumer(AsyncWebsocketConsumer):
    storage = RedisChatStorage()

    @database_sync_to_async
    def check_authentication(self):
        user = self.scope.get('user', AnonymousUser())
        return user.is_authenticated
    
    @database_sync_to_async
    def save_groupmessage(self, message, GM_type = 'normal'):
        print(message)
        GroupMessage.objects.create(
            sender=AUser.objects.get(id=self.user.id),
            is_private=message['is_private'],
            channel=ChannelOfChat.objects.get(urlCode=self.channel_cid),
            _type=GM_type,
            content=json.dumps(message)
        )
        return True

    @require_login
    async def connect(self):
        self.channel_cid = self.scope['url_route']['kwargs']['channel_cid']
        self.room_channel_name = f'chat_{self.channel_cid}'
        self.user = self.scope['user']
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_channel_name,
            self.channel_name
        )

        
        # Add user to active users
        if self.storage.is_user_in_channel(self.channel_cid, self.user.id):
            self.storage.add_active_user(self.channel_cid, self.user.id)

        await self.accept()

        # Notify others about new user
        await self.channel_layer.group_send(
            self.room_channel_name,
            {
                'type': 'user_join',
                'username': self.user.username
            }
        )

    async def disconnect(self, close_code):
        # Remove user from active users
        self.storage.remove_user(self.channel_cid, self.user.id)

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_channel_name,
            self.channel_name
        )

        # Notify others about user leaving
        await self.channel_layer.group_send(
            self.room_channel_name,
            {
                'type': 'user_leave',
                'username': self.user.username
            }
        )


    @require_login
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if text_data_json.get('command') == 'get_active_users':
            await self.get_active_users(None)
            return
        message = text_data_json['message']

        try:
            chat_msg = await self.save_groupmessage(message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_channel_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.user.username
                }
            )
        except Exception as e:
            raise e
            await self.send(text_data=json.dumps({
                'error': 'Failed to save message'
            }))
            print(f'Error saving msg: {e}')


    @require_login
    async def chat_message(self, event):
        print(f'Msg: {event}')
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'username': username
        }))

    async def user_join(self, event):
        # Send message about new user to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_join',
            'username': event['username']
        }))

    async def user_leave(self, event):
        # Send message about user leaving to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'username': event['username']
        }))

    @require_login
    async def get_active_users(self, event):
        # Send list of active users to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'active_users',
            'users': list(self.active_users.get(self.room_channel_name, []))
        }))