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

    async def add_active_user(self, channel_cid, user_id):
        await self.redis.sadd(f'active_users:{channel_cid}', user_id)

    async def remove_user(self, channel_cid, user_id):
        return await self.redis.srem(f'active_users:{channel_cid}', user_id)

    async def get_active_users(self, channel_cid):
        key = f'active_users:{channel_cid}'
        exists = await self.redis.exists(key)
        if exists:
            return await self.redis.smembers(key)
        else:
            return None  # or an empty list, or however you want to handle this case

    async def is_channel_exist(self, channel_cid):
        return await self.redis.exists(f'active_users:{channel_cid}')

    async def is_user_in_channel(self, channel_cid, user_id):
        return await self.redis.sismember(f'active_users:{channel_cid}', user_id)
    

class CassandraChatStorage(ChatStorage):
    def __init__(self, cassandra_session):
        self.session = cassandra_session

    async def add_active_user(self, channel, user):
        # Implement Cassandra-specific logic
        pass