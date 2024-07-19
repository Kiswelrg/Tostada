import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
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

    # storage_initialized = False
    # @classmethod
    # async def initialize_storage(cls):
    #     if not cls.storage_initialized:
    #         await cls.storage.initialize()
    #         cls.storage_initialized = True


    @database_sync_to_async
    def check_authentication(self):
        return True
        user = self.scope.get('user', AnonymousUser())
        return user.is_authenticated
    
    @database_sync_to_async
    def save_message(self):
        print('Save msg to db...')
        return True

    @require_login
    async def connect(self):
        self.channel_cid = self.scope['url_route']['kwargs']['channel_cid']
        self.room_group_name = f'chat_{self.channel_cid}'
        self.user = self.scope['user']

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Add user to active users
        if self.room_group_name not in self.active_users:
            self.active_users[self.room_group_name] = set()
        self.active_users[self.room_group_name].add(self.user.username)

        await self.accept()

        # Notify others about new user
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'username': self.user.username
            }
        )

    async def disconnect(self, close_code):
        # Remove user from active users
        if self.room_group_name in self.active_users:
            self.active_users[self.room_group_name].remove(self.user.username)
            if not self.active_users[self.room_group_name]:
                del self.active_users[self.room_group_name]

        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        # Notify others about user leaving
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'username': self.user.username
            }
        )


    @require_login
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json.get('command') == 'get_active_users':
            await self.get_active_users(None)
            return
        message = text_data_json['message']

        try:
            chat_msg = await self.save_message()

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': self.user.username
                }
            )
        except Exception as e:
            await self.send(text_data=json.dumps({
                'error': 'Failed to save message'
            }))
            print(f'Error saving msg: {e}')


    @require_login
    async def chat_message(self, event):
        print(f'E: {event}')
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
            'users': list(self.active_users.get(self.room_group_name, []))
        }))