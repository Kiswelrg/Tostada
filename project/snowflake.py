# project/snowflake.py

import time
from django.conf import settings

DISCORD_EPOCH = 1704067200000
BUCKET_SIZE = 1000 * 60 * 60 * 24 * 10


def make_bucket(snowflake_id):
   if snowflake_id is None:
       timestamp = int(time.time() * 1000) - DISCORD_EPOCH
   else:
       # When a Snowflake is created it contains the number of
       # seconds since the DISCORD_EPOCH.
       timestamp = snowflake_id >> 22
   return int(timestamp / BUCKET_SIZE)

  
def make_buckets(start_id, end_id=None):
   return range(make_bucket(start_id), make_bucket(end_id) + 1)


class SnowflakeIDGenerator:
    epoch = DISCORD_EPOCH  # Unix timestamp for 2024-01-01 00:00:00 UTC
    machine_id = getattr(settings, 'SNOWFLAKE_MACHINE_ID', 0)
    def __init__(self):
        self.sequence = 0
        self.last_timestamp = 0
        self.test_time = time.time()

    def generate(self):
        current_time = int(time.time() * 1000)
        timestamp = current_time - self.epoch

        if timestamp < 0:
            raise ValueError("Clock moved backwards. Refusing to generate ID.")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 4095
            if self.sequence == 0:
                while timestamp <= self.last_timestamp:
                    timestamp = int(time.time() * 1000) - self.epoch
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        return (timestamp << 22) | (self.machine_id << 12) | self.sequence

# Global instance
# snowflake_generator = SnowflakeIDGenerator()


# Tool app
tool_server_snowflake_generator = SnowflakeIDGenerator()
def getToolServerSnowflakeID():
    return tool_server_snowflake_generator.generate()

tool_channelofchat_snowflake_generator = SnowflakeIDGenerator()
def getToolChannelOfChatSnowflakeID():
    return tool_channelofchat_snowflake_generator.generate()

tool_channelofvoice_snowflake_generator = SnowflakeIDGenerator()
def getToolChannelOfVoiceSnowflakeID():
    return tool_channelofvoice_snowflake_generator.generate()

tool_categoryinserver_snowflake_generator = SnowflakeIDGenerator()
def getToolCategoryInServerSnowflakeID():
    return tool_categoryinserver_snowflake_generator.generate()


# Message app
message_message_snowflake_generator = SnowflakeIDGenerator()
def getMessageMessageSnowflakeID():
    return message_message_snowflake_generator.generate()

message_directmessage_snowflake_generator = SnowflakeIDGenerator()
def getMessageDirectMessageSnowflakeID():
    return message_directmessage_snowflake_generator.generate()

message_groupmessage_snowflake_generator = SnowflakeIDGenerator()
def getMessageGroupMessageSnowflakeID():
    return message_groupmessage_snowflake_generator.generate()


# Account app
account_auser_snowflake_generator = SnowflakeIDGenerator()
def getAccountAUserSnowflakeID():
    return account_auser_snowflake_generator.generate()


# Attachment app
attachment_gmfile_snowflake_generator = SnowflakeIDGenerator()
def AttachmentGMFileSnowflakeID():
    return attachment_gmfile_snowflake_generator.generate()
