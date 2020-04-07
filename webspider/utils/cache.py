# coding=utf-8
import logging
import pickle
from functools import wraps

import redis

from webspider import setting

redis_pool = redis.ConnectionPool(host=setting.REDIS_CONF['host'],
                                  port=setting.REDIS_CONF['port'])
redis_instance = redis.Redis(connection_pool=redis_pool)


def simple_cache(ex=None):
    """利用 redis 进行缓存，暂不支持 kwargs 类型的参数传入方式"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if kwargs:
                raise ValueError(
                    "args key generator does not accept kwargs arguments")
            redis_key = func.__name__ + '(' + ','.join(map(str, args)) + ')'
            result = redis_instance.get(redis_key)
            if result:
                logging.debug('cache: get func result from redis key - {}'.format(redis_key))
                result = pickle.loads(result)
            else:
                logging.debug('cache: get func result from func key - {}'.format(redis_key))
                result = func(*args)
                redis_instance.set(name=redis_key, value=pickle.dumps(result), ex=ex)
            return result

        return wrapper

    return decorator


def cache_clear(func, *args):
    """失效缓存"""
    redis_key = func.__name__
    if args:
        redis_key += ('(' + ','.join(map(str, args)) + ')')
    logging.info('remove cache redis-key: {}'.format(redis_key))
    keys = redis_instance.keys('*' + redis_key + '*')
    if keys:
        remove_count = redis_instance.delete(*keys)
        logging.info('cache clear count {}'.format(remove_count))
        return remove_count
