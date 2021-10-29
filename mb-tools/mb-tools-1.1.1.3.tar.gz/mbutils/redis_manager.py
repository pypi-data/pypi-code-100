import redis
class RedisManager:
    """
        redis封装, redis特殊业务需要使用主从
    """
    def __init__(self, redis_config):
        """
        :param redis_config:
            {
                "host":"pre.xiaoantech.com",
                "port": 6379,
                "pwd" :"",
                "db" : 0
            }
        """
        if redis_config:
            self.connect_pool = redis.ConnectionPool(host=redis_config['host'],
                                                     port=redis_config['port'],
                                                     password=redis_config['pwd'],
                                                     db=redis_config.get('db', 0) + redis_config["is_test_env"],
                                                     max_connections=redis_config["redis_max_num"], decode_responses=True)

            print("RedisManager,env:", redis_config["is_test_env"], flush=True)
            self.r = redis.Redis(connection_pool=self.connect_pool, decode_responses=True)
