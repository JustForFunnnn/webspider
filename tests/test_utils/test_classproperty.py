# coding=utf-8
from unittest import TestCase

from webspider.utils.classproperty import classproperty


class TestClass(object):
    _name = '阿河'

    @classproperty
    def name(cls):
        return cls._name


class TestUtilClassProperty(TestCase):
    def test_read_class_property(self):
        self.assertEqual(TestClass.name, '阿河')
