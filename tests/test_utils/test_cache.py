# coding=utf-8
import time
from unittest import TestCase

from webspider.utils.cache import simple_cache, cache_clear, redis_instance

test_number = 0


@simple_cache()
def incr_then_return_test_number(keyword=None):
    global test_number
    test_number += 1
    return test_number


@simple_cache(ex=1)
def incr_then_return_test_number_with_ex(keyword=None):
    global test_number
    test_number += 1
    return test_number


class TestClass(object):
    def __init__(self, name):
        self.name = name


class TestCache(TestCase):

    def setUp(self):
        keys = redis_instance.keys('*incr_then_return_test_number*')
        if keys:
            redis_instance.delete(*keys)

        keys = redis_instance.keys('*return_what_you_put*')
        if keys:
            redis_instance.delete(*redis_instance.keys('*return_what_you_put*'))

    def test_simple_cache(self):
        """测试缓存"""
        global test_number
        test_number = 0
        self.assertEqual(1, incr_then_return_test_number('test'))
        self.assertEqual(1, incr_then_return_test_number('test'))
        self.assertEqual(2, incr_then_return_test_number('test_1'))
        self.assertEqual(2, incr_then_return_test_number('test_1'))
        self.assertEqual(3, incr_then_return_test_number('test_2'))

        with self.assertRaises(ValueError):
            incr_then_return_test_number(keyword='test')

    def test_simple_cache_with_ex(self):
        """测试设置了过期时间的缓存"""
        global test_number
        test_number = 0
        self.assertEqual(1, incr_then_return_test_number_with_ex('test'))
        self.assertEqual(1, incr_then_return_test_number_with_ex('test'))
        time.sleep(1)
        self.assertEqual(2, incr_then_return_test_number_with_ex('test'))

    def test_cache_clear(self):
        """测试清除缓存"""
        global test_number
        test_number = 0
        self.assertEqual(1, incr_then_return_test_number('test'))
        self.assertEqual(2, incr_then_return_test_number('test_1'))
        cache_clear(incr_then_return_test_number)
        self.assertEqual(3, incr_then_return_test_number('test'))
        self.assertEqual(4, incr_then_return_test_number('test_1'))

    def test_cache_class_instance(self):
        """测试缓存类实例"""

        @simple_cache()
        def return_what_you_input(whatever):
            return whatever

        instance = TestClass('测试类实例')
        # cache class
        instance = return_what_you_input(instance)
        # get result from redis
        cache_instance = return_what_you_input(instance)
        self.assertTrue(instance is not cache_instance)
        self.assertTrue(isinstance(cache_instance, TestClass))
        self.assertEqual(cache_instance.name, '测试类实例')

    def tearDown(self):
        keys = redis_instance.keys('*incr_then_return_test_number*')
        if keys:
            redis_instance.delete(*redis_instance.keys('*incr_then_return_test_number*'))

        keys = redis_instance.keys('*return_what_you_put*')
        if keys:
            redis_instance.delete(*redis_instance.keys('*return_what_you_put*'))
