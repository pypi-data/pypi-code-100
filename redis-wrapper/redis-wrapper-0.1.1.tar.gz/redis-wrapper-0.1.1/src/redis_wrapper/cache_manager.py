import redis

class CacheManager:
    rds: redis.Redis = None
    pubsub = None

    @staticmethod
    def Init(host: str, port: str):
        CacheManager.rds = redis.Redis(host=host,port=port)
        CacheManager.pubsub = CacheManager.rds.pubsub()

    @staticmethod
    def Get(key: str):
        ret = CacheManager.rds.get(key)
        if(ret != None):
            ret = ret.decode("utf-8")

        return ret
        
    @staticmethod
    def Set(key: str, value: str):
        CacheManager.rds.set(key,value)

    @staticmethod
    def Publish(channel: str, message: str):
        return CacheManager.rds.publish(channel, message)

    @staticmethod
    def Subscribe(pattern: str, handler, thread_sleep_time = 0.01):
        #subscribe_key = '*'
        CacheManager.pubsub.psubscribe(**{pattern: handler})
        CacheManager.pubsub.run_in_thread(sleep_time=thread_sleep_time)        
