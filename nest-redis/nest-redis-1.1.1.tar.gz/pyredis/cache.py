# -*- coding: utf-8 -*-
import redis
import json
import pickle


class RedisUtil:
    # 初始化
    def __init__(self, config: dict) -> None:
        pool = redis.ConnectionPool(
            **config
        )
        self.r = redis.Redis(connection_pool=pool)

    #############################################################
    #              字符串相关                                     #
    #############################################################
    def set(self, key: str, val: object, time: int = -1) -> None:
        '''
        字符串添加
        :param key: string
        :param val:  dict,list or string,int
        :param expir: int 默认为-1 永久有效
        :return: None
        '''
        val = str(pickle.dumps(val))
        self.r.set(key, val, ex=time) if time > -1 else self.r.set(key, val)

    # 字符串读取
    def get(self, name: str) -> object:
        '''
        :param name: string
        :return: string or dict or list
        '''
        data = self.r.get(name)
        return pickle.loads(eval(data)) if data else ""

    # 获取ttl
    def ttl(self, name: str) -> int:
        '''
        :param name: string
        :return:  int 剩余时间
        '''
        return self.r.ttl(name)

    # 移除过期时间
    def persist(self, name: str) -> int:
        '''
        移除key的过期时间
        :param name: string key名称
        :return: int -1移除成功 0 移除失败
        '''
        return self.r.persist(name) or 0

    # 设置key的过期时间
    def expire(self, name: str, time: int = 7200) -> int:
        '''
        :param name: string key的名称
        :param time: int 秒 默认7200秒
        :return: 0添加失败 1：添加成功
        '''
        return self.r.expire(name, time)

    #############################################################
    #                哈希相关                                     #
    #############################################################
    def hget(self, name: str, key: str) -> object:
        '''
        hash 读取
        :param name: string hash的名称
        :param key:  string hash的key
        :return: object
        '''
        try:
            return json.loads(self.r.hget(name, key))
        except:
            return self.r.hget(name, key) or None

    def hgetall(self, name: str) -> dict:
        '''
        hash 读取全部
        :param name: string hash的名称
        :return: dict
        '''
        return self.r.hgetall(name) or {}

    def hset(self, name: str, key: str, val: object) -> int:
        '''
        hash 添加
        :param name: string hash的名称
        :param key:  string hash的key
        :param val:  object hash的值
        :return: int 1:添加成功 0:添加失败
        '''
        if isinstance(val, list) or isinstance(val, dict):
            val = json.dumps(val)
        return self.r.hset(name, key, val)

    def hlen(self, name: str) -> int:
        '''
        获取hash的长度
        :param name: hash的名称
        :return: hash的长度
        '''
        return self.r.hlen(name) or 0

    def hmset(self, name: str, mapping: dict = {}) -> bool:
        '''
        hash 批量添加
        :param name: string  hash的名称
        :param mapping: dict  {key: val}
        :return: Boolean
        '''
        return self.r.hmset(name, mapping)

    def hdel(self, name: str, key: str) -> int:
        '''
        hash 删除数据
        :param name: string  hash的名称
        :param key:  string  hash的key
        :return: int 0:删除失败 1：删除成功
        '''
        return self.r.hdel(name, key)

    def hexists(self, name: str, key: str) -> bool:
        '''
        hash 判断key是否存在
        :param name: string hash的名称
        :param key: string hash的字段值
        :return: bool  返回布尔值，存在返回True,否则返回False
        '''
        return self.r.hexists(name, key)

    #############################################################
    #                队列相关                                     #
    #############################################################
    def lpush(self, name: str, val: object) -> int:
        '''
        list 添加数据,从左侧添加数据
        :param name: string 列表的key
        :param val: list ["1","2"]列表的值
        :return: int 索引值
        '''
        if isinstance(val, list):
            return self.r.lpush(name, *val)
        return self.r.lpush(name, val)

    def rpop(self, name: str) -> object:
        '''
        list 删除数据，从右侧删除数据
        :param name: 队列的名称
        :return: 返回删除队列的值
        '''
        return self.r.rpop(name)

    def llen(self, name: str) -> int:
        '''
        计算队列的长度
        :param name: 队列的名称
        :return: int 返回队列的长度
        '''
        return self.r.llen(name)

    #############################################################
    #               有序集合相关                                  #
    #############################################################
    def zadd(self, name: str, mapping: dict) -> int:
        '''
        zset 添加有序集合数据
        :param name: string 有序集合的key
        :param mapping: dict  有序集合的值 { key: score}
        :return: int 添加的个数
        '''
        return self.r.zadd(name, mapping)

    def card(self, name: str) -> int:
        '''
        zset 获取有序集合的个数
        :param name: string 有序集合的名称
        :return: int 有序集合内容的个数
        '''
        return self.r.zcard(name)

    def zrange(self, name: str, start: int = 0, end: int = -1) -> list:
        '''
        zset 获取有序集合的数据
        :param name: string 有序集合的名称
        :param start: 数据的起始位置(默认为0)
        :param end: 数据的结束位置(默认为-1)
        :return: list 返回数据
        '''
        return self.r.zrange(name, start, end)

    def zscan_iter(self, key: str, match: str = "*") -> list:
        '''
        有序集合的过滤 默认获取所有
        :param key:  有序集合的key
        :param match:  匹配条件
        :return: List 匹配的键
        '''
        return [i[0] for i in self.r.zscan_iter(key, match=match)]

    def zrank(self, name: str, value: str) -> int:
        '''

        :param name: 有序集合的key
        :param value: 需要查看的值
        :return: 返回的索引值,如果是None则不存在
        '''
        index = self.r.zrank(name, value)
        return index if index != None else -1

    def zcard(self, name: str) -> int:
        '''
        获取有序集合的长度
        :param name:有序集合的键
        :return: 返回有序集合的长度
        '''
        return self.r.zcard(name)

    def zrem(self, name: str, *val: object) -> int:
        '''
        删除有序集合中的元素
        :param name: 有序集合的名称
        :param val: 有序集合的值，不定长参数
        :return: 删除的个数
        '''
        return self.r.zrem(name, *val)

    #############################################################
    #                集合相关                                     #
    #############################################################
    def sadd(self, name: str, *value: object) -> int:
        '''
        添加数据到集合中
        :param name: 集合的名称
        :param value: 集合的值
        :return: 1添加成功 0 添加失败
        '''
        return self.r.sadd(name, *value)

    def scard(self, name: str) -> int:
        '''
        计算集合的长度
        :param name: 集合的名称
        :return: 集合的长度
        '''
        return self.r.scard(name)

    def smembers(self, name: str) -> set:
        '''
        查看集合中的数据
        :param name: 集合的名称
        :return: set 返回数据的集合
        '''
        return self.r.smembers(name)

    def sdiff(self, A: set, B: set) -> set:
        '''
        返回集合的差集,已属于A而不属于B的元素称为A与B的差
        :param A:
        :param B:
        :return: set 返回的差集
        '''
        return self.r.sdiff(A, B)

    def sinter(self, A: set, B: set) -> set:
        '''
        获取集合的交集,属于A且属于B的交(集)
        :param A:
        :param B:
        :return: set
        '''
        return self.r.sinter(A, B)

    def sunion(self, A: set, B: set) -> set:
        '''
        获取集合的并集：已属于A或属于B的元素为称为A与B的并
        :param A:
        :param B:
        :return:
        '''
        return self.r.sunion(A, B)

    def sismember(self, name: str, val: object) -> bool:
        '''
        查询 一个元素是否在集合中
        :param name: 集合的名称
        :param val: 要查找的元素的值
        :return: bool
        '''
        return self.r.sismember(name, val)

    def srem(self, name: str, *val: object) -> int:
        '''
        删除元素中的值
        :param name: 集合的名称
        :param val: 集合的值，不定长参数
        :return: 返回删除的个数
        '''
        return self.r.srem(name, *val)

    #############################################################
    #                其他相关                                     #
    #############################################################
    def handler(self) -> object:
        '''
        返回句柄
        :return: redis句柄
        '''
        return self.r

    def flushdb(self) -> bool:
        '''
        清空数据库
        :return: bool
        '''
        return self.r.flushdb()

    def delete(self, key: str) -> int:
        '''
        删除 key
        :param key: string => redis的key值
        :return: int
        '''
        return self.r.delete(key)

    def keys(self, pattern: str = "*") -> list:
        '''
        匹配数据库中的键
        :param pattern: string => 表达式，默认为*
        :return: list
        '''
        return self.r.keys(pattern)
