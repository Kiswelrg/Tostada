import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from django.http.response import Http404
from .models import ChatMessage
from attachment.models import MFile
from tool.models import ChannelOfChat
from account.models import AUser
from .Storage.chat import RedisChatStorage
import base64
from io import BytesIO
from PIL import Image

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
    def getAttachments(self, m, attrs=None):
        if attrs is None:
            attrs = ['name', 'url']
        return [
            MFile.get_file(a.urlCode, attrs=attrs) for a in m.attachments.all()
        ]
    

    @database_sync_to_async
    def check_authentication(self):
        user = self.scope.get('user', AnonymousUser())
        return user.is_authenticated
    

    @database_sync_to_async
    def save_groupmessage(self, message, files, GM_type = 'normal'):
        msg = ChatMessage.objects.create(
            sender=AUser.objects.get(id=self.user.id),
            is_private=message['is_private'],
            channel=ChannelOfChat.objects.get(urlCode=self.channel_cid),
            _type=GM_type,
            contents=json.dumps(message['contents'])
        )
        for f in files:
            MFile.objects.create(
                file=f,
                message=msg
            )
        return msg

    @require_login
    async def connect(self):
        if self.storage.redis is None:
            await self.storage.initialize()
        self.channel_cid = self.scope['url_route']['kwargs']['channel_cid']
        
        self.room_channel_name = f'chat_{self.channel_cid}'
        self.user = self.scope['user']
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_channel_name,
            self.channel_name
        )

        
        # Add user to active users
        if await self.storage.is_user_in_channel(self.channel_cid, self.user.id):
            await self.storage.add_active_user(self.channel_cid, self.user.id)

        await self.accept()

        # Notify others about new user
        await self.channel_layer.group_send(
            self.room_channel_name,
            {
                'type': 'user_join',
                'data': [
                    {'username': self.user.username}
                ]
            }
        )
        await self.fetch_messages()

    async def disconnect(self, close_code):
        # Remove user from active users
        await self.storage.remove_user(self.channel_cid, self.user.id)

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
                'data': [
                    {'username': self.user.username}
                ]
            }
        )

    @require_login
    async def fetch_messages(self):
        
        if not self.storage.is_channel_exist(self.channel_cid):
            await self.send(text_data=json.dumps({
                'error': 'Channel does not exist'
            }))
            return
        

        @database_sync_to_async
        def get_messages():
            # try:
            channel = get_object_or_404(ChannelOfChat, urlCode=self.channel_cid)
            # except Http404:
            #     return []
            return list(channel.all_msgs.all()[:50])  # Use .all() before slicing

        msgs = await get_messages()

        await self.channel_layer.group_send(
            self.room_channel_name,
            {
                'type': 'history_message',
                'messages': [{
                    'sender': {
                        'username': await database_sync_to_async(lambda: msg.sender.username)(),
                        'avatar': await database_sync_to_async(lambda: get_object_or_404(AUser, id=msg.sender.id).avatar.url)()
                    },
                    'mentioned_user': {},
                    'tool_used': {},
                    'time_sent': msg.time_sent.isoformat(),
                    'type': msg._type,
                    'cid': str(msg.urlCode),
                    'is_edited': {
                        'state': msg.is_edited,
                        'text': 'edited',
                        'last_edit':msg.last_edit.isoformat(),
                    },
                    'is_private': msg.is_private,
                    'contents': json.loads(msg.contents), # load in frontend, save some performance for Django
                    'attachments': await self.getAttachments(msg)
                } for msg in msgs]
                
            }
        )

    def decode_base64(self, data):
        try:
            file_bytes = base64.b64decode(data)
            return file_bytes
        except base64.binascii.Error as e:
            raise ValueError("Error decoding base64 data: " + str(e))


    def process_generic_file(self, file_data, file_name):

        try:
            with open(f'/path/to/save/{file_name}', 'wb') as file:
                file.write(file_data)
            return f'/path/to/save/{file_name}'
        except IOError as e:
            raise ValueError("Error saving file: " + str(e))
    def process_image(self, file_data):
        try:
            image = Image.open(BytesIO(file_data))
            # You can now work with the image object
            # For example, save it to a file:
            # image.save(f'/path/to/save/{file_name}')
            return image
        except IOError as e:
            raise ValueError("Error constructing image from bytes: " + str(e))
    def process_file(self, file_data, file_type, file_name):
        # if file_type.startswith('image/'):
        #     return self.process_image(file_data)
        # else:
        return self.process_generic_file(file_data, file_name)


    @require_login
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        if text_data_json.get('command') == 'get_active_users':
            await self.get_active_users(None)
            return
        if text_data_json.get('command') == 'delete_message':
            await self.delete_message(text_data_json['cid'])
            return
        message = text_data_json['message']
        msg_files = text_data_json['message']['files']
        

        files = []
        for file in msg_files:
            file_data_base64 = file['data']
            file_type = file['type']
            file_name = file['name']


            # Process the file based on its type
            # processed_file = self.process_file(file_data, file_type, file_name)
            try:
                # Decode Base64 data
                file_data = self.decode_base64(file_data_base64)
                files.append(
                    ContentFile(file_data, name = file_name)
                )
                print(f'File {file_name} ready to save.')
            except ValueError as e:
                print("Error processing file:", e)
        # try:
        msg = await self.save_groupmessage(message, files)

        # Send message to room group
        get_file_async = sync_to_async(MFile.get_file)


        await self.channel_layer.group_send(
            self.room_channel_name,
            {
                'type': 'chat_message',
                'messages': [{
                    'sender': {
                        'username': await database_sync_to_async(lambda: msg.sender.username)(),
                        'avatar': await database_sync_to_async(lambda: get_object_or_404(AUser, id=msg.sender.id).avatar.url)()
                    },
                    'mentioned_user': {},
                    'tool_used': {},
                    'time_sent': msg.time_sent.isoformat(),
                    'type': msg._type,
                    'cid': msg.urlCode,
                    'is_edited': {
                        'state': msg.is_edited,
                        'text': 'edited',
                        'last_edit':msg.last_edit.isoformat(),
                    },
                    'is_private': msg.is_private,
                    'contents': json.loads(msg.contents), # load in frontend, save some performance for Django
                    'attachments': await self.getAttachments(msg)
                }]
                
            }
        )
        # except Exception as e:
        #     raise e
        #     await self.send(text_data=json.dumps({
        #         'error': 'Failed to save message'
        #     }))
        #     print(f'Error saving msg: {e}')

    
    @require_login
    async def delete_message(self, message_cid):
        @database_sync_to_async
        def delete_message_from_db():
            message = ChatMessage.objects.get(urlCode=message_cid, sender__id=self.user.id)
            message.delete()
            return True
            
        u = self.user
        try:
            # sender = await database_sync_to_async(lambda: ChatMessage.objects.get(urlCode=message_cid).sender.id)()
            sender = await database_sync_to_async(lambda: get_object_or_404(ChatMessage, urlCode = message_cid).sender.id)()
        
            # Check if the user is authorized to delete the message
            if sender != u.id:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'error': 'Unauthorized: You cannot delete this message.'
                }))
                return
            
            hasAuth = True
            success = await delete_message_from_db()
            await self.channel_layer.group_send(
                self.room_channel_name,
                {
                    'type': 'message_deleted',
                    'cid': message_cid,
                }
            )
        except ChatMessage.DoesNotExist:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'error': 'Message not found.'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'error': 'Failed to delete message.'
            }))
            print(f'Error deleting message: {e}')


    @require_login
    async def chat_message(self, event):
        msgs = event['messages']
        print(f'Msg: {[msg["contents"] for msg in msgs]}')

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'messages': msgs,
        }))


    @require_login
    async def history_message(self, event):
        msgs = event['messages']
        print(f'Msg: {[msg["contents"][0]["content"] for msg in msgs]}')
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'history_message',
            'messages': msgs,
        }))

    @require_login
    async def message_deleted(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message_deleted',
            'cid': event['cid'],
        }))


    async def user_join(self, event):
        # Send message about new user to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_join',
            'users': [
                {
                    'username': user['username']
                } for user in event['data']
            ]
        }))


    async def user_leave(self, event):
        # Send message about user leaving to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'users': [
                {
                    'username': user['username']
                } for user in event['data']
            ]
        }))


    @require_login
    async def get_active_users(self, event):
        # Send list of active users to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'active_users',
            'users': list(self.active_users.get(self.room_channel_name, []))
        }))
