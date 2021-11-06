from .default_settings import *

SCHEDULER_PRESIST = False
ASYNC_TYPE = 'coroutine'
MAX_ASYNC_NUMBER = 2

# redis queue
REDIS_QUEUE_NAME = 'spider_queue'
REDIS_QUEUE_HOST = 'localhost'
REDIS_QUEUE_PORT = 6379
REDIS_QUEUE_DB = 2
REDIS_QUEUE_PASSWORD = None

# set
REDIS_SET_NAME = 'spider_set'
REDIS_SET_HOST = 'localhost'
REDIS_SET_PORT = 6379
REDIS_SET_DB = 2
REDIS_SET_PASSWORD = None

# backup
REDIS_BACKUP_NAME = 'spider_backup'
REDIS_BACKUP_HOST = 'localhost'
REDIS_BACKUP_PORT = 6379
REDIS_BACKUP_DB = 2
REDIS_BACKUP_PASSWORD = None

# role
ROLE = 'master'


try:
    from settings import *
except:
    pass

