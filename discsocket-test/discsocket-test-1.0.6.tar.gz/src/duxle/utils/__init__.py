from .cdn import return_cdn_avatar

# Set interaction opcodes
DISPATCH = 0
HEARTBEAT = 1
IDENTIFY = 2
RESUME = 6
RECONNECT = 7
INVALID_SESSION = 9
HELLO = 10
HEARTBEAT_ACK = 11  

# Set application command types
SLASH = 1
USER = 2
MESSAGE = 3

__version__ = '1.0.4'