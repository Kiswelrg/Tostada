from rest_framework import serializers
from .models import ChatMessage, DirectMessage
from account.models import AUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AUser
        fields = ['id', 'username', 'avatar', 'is_online']


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    mentioned_user = UserSerializer(read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = [
            'urlCode', 'contents', 'time_sent', 'is_read', 'is_edited', 
            'last_edit', 'sender', 'mentioned_user', 'is_private', 
            'channel', 'tool_used', 'state'
        ]


class DirectMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    
    class Meta:
        model = DirectMessage
        fields = [
            'urlCode', 'contents', 'time_sent', 'is_read', 'is_edited',
            'last_edit', 'sender', 'receiver'
        ]


class RoomSerializer(serializers.Serializer):
    channel_id = serializers.CharField()
    room_type = serializers.CharField()  # 'direct' or 'channel'
    name = serializers.CharField()
    last_message = serializers.CharField(allow_null=True)
    last_message_time = serializers.DateTimeField(allow_null=True)
    unread_count = serializers.IntegerField()
    participants = UserSerializer(many=True, read_only=True)