# Message pagination configuration
# These constants control message loading and caching behavior

# Initial message load when connecting to a channel
INITIAL_MESSAGE_LIMIT = 50

# Number of messages to fetch per pagination request
PAGINATION_MESSAGE_LIMIT = 30

# Maximum messages to keep in frontend cache
# Note: This is used by frontend but defined here for consistency
MAX_MESSAGE_CACHE_SIZE = 200

# Maximum files per message
MAX_FILES_PER_MESSAGE = 10

# Maximum total file size per message (in bytes)
MAX_FILE_SIZE_TOTAL = 512 * 1024 * 1024  # 512 MB