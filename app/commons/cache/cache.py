import pickle
from typing import Any

from redis import ConnectionPool, Redis
from flask import current_app


# redis中需要添加键的方法, 单键, 只处理5种基础类型
single_key = {
    'set', 'setnx', 'setex', 'psetex', 'get', 'getset', 'strlen', 'append', 'setrange', 'getrange', 'incr', 'incrby',
    'incrbyfloat', 'decr', 'decrby',  # String
    'lpush', 'lpushx', 'lrange', 'rpush', 'rpushx', 'lpop', 'rpop', 'lrem', 'llen', 'lindex', 'linsert', 'lset',
    'ltrim',  # list
    'hdel', 'hexists', 'hget', 'hgetall', 'hincrby', 'hincrbyfloat', 'hkeys', 'hlen', 'hset', 'hsetnx', 'hmset',
    'hmget', 'hvals', 'hstrlen', 'hscan',  # hash
    'sadd', 'scard', 'sismember', 'smembers', 'spop', 'srandmember', 'srem', 'sscan', 'sdiffstore', 'sinterstore',
    'sunionstore',  # set
    'zadd', 'zcard', 'zcount', 'zincrby', 'zlexcount', 'zpopmax', 'zpopmin', 'zrange', 'zrangebylex', 'zrevrangebylex',
    'zrangebyscore', 'zrank', 'zrem', 'zremrangebylex', 'zremrangebyrank', 'zremrangebyscore', 'zrevrange',
    'zrevrangebyscore', 'zrevrank', 'zscore', 'zscan', 'zinterstore', 'zunionstore'  # zset
}

multi_keys = {
    'mget', 'blpop', 'brpop', 'sdiff', 'sinter', 'sunion', 'bzpopmax', 'bzpopmin'
}

mapping_keys = {
    'mset', 'msetnx'
}

# 两个键: src, dest
special_keys = {
    'rpoplpush', 'brpoplpush', 'smove'
}


class ProxyClient(object):
    """只处理第一个参数是key 或 keys 的redis原生方法, 并会带上参数, 否则还是用原生方法"""
    def __init__(self, client: Redis, key_prefix):
        self.client = client
        self.key_prefix = key_prefix

    def __getattr__(self, item):
        """本来可以做一个判断筛选, 哪些方法自动去加前缀, 现在统一处理"""
        if hasattr(Redis, item):
            return self.handle(item)
        return super().__getattr__(item)

    def handle(self, item):
        # 只处理第一个参数是name的方法
        def inner(*args, **kwargs):
            # 如果第一个参数是name
            method = getattr(self.client, item)
            if item in single_key:
                key = f'{self.key_prefix}{args[0]}'
                return method(key, *args[1:], **kwargs)
            elif item in multi_keys:
                keys = [f'{self.key_prefix}{key}' for key in args[0]]
                return method(keys, *args[1:], **kwargs)
            elif item in mapping_keys:
                # 参数是一个键一个value
                new_args = args[0].copy()
                for key, value in args[0].items():
                    value = new_args.pop(key)
                    new_args[f'{self.key_prefix}{key}'] = value
                return method(new_args, *args[1:], **kwargs)
            elif item in special_keys:
                # 参数是一个src 一个dst
                arg1 = f'{self.key_prefix}{args[0]}'
                arg2 = f'{self.key_prefix}{args[1]}'
                return method(arg1, arg2, *args[2:], **kwargs)
            else:
                return method(*args, **kwargs)
        return inner


class BaseCache(object):
    cache_settings = current_app.config['CACHE_SETTINGS']
    key_prefix = cache_settings.get('PREFIX', '')  # 获取前缀

    @classmethod
    def _get_redis_pool(cls) -> ConnectionPool:
        if not hasattr(cls, '_redis_pool'):
            cls._redis_pool = ConnectionPool(host=cls.cache_settings.get('HOST', ),
                                             port=cls.cache_settings.get('PORT'),
                                             db=cls.cache_settings.get('DB'))
        return cls._redis_pool

    @classmethod
    def client(cls) -> Redis:
        """原生redis客户端"""
        if not hasattr(cls, '_client'):
            cls._client = Redis(connection_pool=cls._get_redis_pool())
        return cls._client

    @classmethod
    def prefix_client(cls, **kwargs) -> Redis:
        """带上前缀的原生客户端"""
        if not hasattr(cls, '_prefix_client'):
            if not hasattr(cls, '_prefix_redis_pool'):
                decode_responses = kwargs.pop('decode_responses', True)
                cls._prefix_redis_pool = ConnectionPool(host=cls.cache_settings.get('HOST'),
                                                        port=cls.cache_settings.get('PORT'),
                                                        db=cls.cache_settings.get('DB'),
                                                        decode_responses=decode_responses,
                                                        **kwargs)
            _client = Redis(connection_pool=cls._prefix_redis_pool)
            cls._prefix_client = ProxyClient(_client, cls.key_prefix)
        return getattr(cls, '_prefix_client')

    @staticmethod
    def _dump_object(value) -> bytes:
        """Dumps an object into a string for redis.  By default it serializes
        integers as regular string and pickle dumps everything else.
        """
        t = type(value)
        if t == int:
            return str(value).encode("ascii")
        return b"!" + pickle.dumps(value)

    @staticmethod
    def _load_object(value: bytes) -> Any:
        """The reversal of :meth:`dump_object`.  This might be called with
        None.
        """
        if value is None:
            return None
        if value.startswith(b"!"):
            try:
                return pickle.loads(value[1:])
            except pickle.PickleError:
                return None
        try:
            return int(value)
        except ValueError:
            return value

    @classmethod
    def delete_with_pickle(cls, key):
        """根据键删除"""
        return cls.client().delete(cls._get_key_with_prefix(key))

    @classmethod
    def get_with_pickle(cls, key):
        """获取并解码"""
        key_with_prefix = cls._get_key_with_prefix(key)
        return cls._load_object(cls.client().get(key_with_prefix))

    @classmethod
    def set_with_pickle(cls, key, value, timeout=None):
        dump = cls._dump_object(value)
        key_with_prefix = cls._get_key_with_prefix(key)
        if timeout == -1:
            result = cls.client().set(key_with_prefix, value=dump)
        else:
            result = cls.client().set(key_with_prefix, value=dump, ex=timeout)
        return result

    @classmethod
    def _get_key_with_prefix(cls, key):
        return '{}{}'.format(cls.key_prefix, key)
