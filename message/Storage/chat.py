from abc import ABC, abstractmethod
from django.conf import settings
import redis

class ChatStorage(ABC):
    @abstractmethod
    async def add_active_user(self, channel, user):
        pass

    @abstractmethod
    async def remove_user(self, channel, user):
        pass

    @abstractmethod
    async def get_active_users(self, channel):
        pass


class InMemoryChatStorage(ChatStorage):
    def __init__(self):
        self.active_users = {}

    async def add_active_user(self, channel, user):
        if channel not in self.active_users:
            self.active_users[channel] = set()
        self.active_users[channel].add(user)

    # ... implement other methods ...


class RedisChatStorage(ChatStorage):
    def __init__(self):
        self.redis = redis.StrictRedis(
            host = settings.CHANNEL_LAYERS['default']['CONFIG']['hosts'][0][0],
            port = settings.CHANNEL_LAYERS['default']['CONFIG']['hosts'][0][1],
            db = 0
        )

    # async def initialize(self):
    #     pass

    async def add_active_user(self, channel_id, user_id):
        await self.redis.sadd(f'active_users:{channel_id}', user_id)

    async def remove_user(self, channel_id, user_id):
        await self.redis.srem(f'active_users:{channel_id}', user_id)

    async def get_active_users(self, channel_id):
        return await self.redis.smembers(f'active_users:{channel_id}')

    async def is_in_channel(self, channel_id, user_id):
        return await self.redis.sismember(f'active_users:{channel_id}', user_id)
    

class CassandraChatStorage(ChatStorage):
    def __init__(self, cassandra_session):
        self.session = cassandra_session

    async def add_active_user(self, channel, user):
        # Implement Cassandra-specific logic
        pass