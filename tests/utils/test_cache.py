# coding=utf-8
from unittest import TestCase

from webspider.utils.cache import simple_cache, cache_clear, redis_instance

test_numbers = 0


@simple_cache
def print_numbers(keyword):
    global test_numbers
    test_numbers += 1
    return test_numbers


class TestClass(object):
    def __init__(self, name):
        self.name = name


class CacheTestCase(TestCase):
    def setUp(self):
        keys = redis_instance.keys('*print_numbers*')
        if keys:
            redis_instance.delete(*keys)

        keys = redis_instance.keys('*return_what_you_put*')
        if keys:
            redis_instance.delete(*redis_instance.keys('*return_what_you_put*'))

    def test_simple_cache(self):
        global test_numbers
        test_numbers = 0
        self.assertEqual(1, print_numbers('test'))
        self.assertEqual(1, print_numbers('test'))
        self.assertEqual(2, print_numbers('test_1'))
        self.assertEqual(2, print_numbers('test_1'))
        self.assertEqual(1, print_numbers('test'))
        self.assertEqual(3, print_numbers('test_2'))

        with self.assertRaises(ValueError):
            print_numbers(keyword='test')

    def test_cache_clear(self):
        global test_numbers
        test_numbers = 0
        self.assertEqual(1, print_numbers('test'))
        self.assertEqual(2, print_numbers('test_1'))
        cache_clear(print_numbers)
        self.assertEqual(3, print_numbers('test'))
        self.assertEqual(4, print_numbers('test_1'))

    def test_cache_class_instance(self):
        @simple_cache
        def return_what_you_put(whatever):
            return whatever

        instance = TestClass('测试类实例')
        # cache class
        return_what_you_put(instance)
        # get result from redis
        cache_instance = return_what_you_put(instance)
        self.assertTrue(isinstance(cache_instance, TestClass))
        self.assertEqual(cache_instance.name, '测试类实例')

    def tearDown(self):
        keys = redis_instance.keys('*print_numbers*')
        if keys:
            redis_instance.delete(*redis_instance.keys('*print_numbers*'))

        keys = redis_instance.keys('*return_what_you_put*')
        if keys:
            redis_instance.delete(*redis_instance.keys('*return_what_you_put*'))
