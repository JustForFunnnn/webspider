# coding=utf-8
from unittest import TestCase

from webspider.exceptions import DowngradeException
from webspider.web.formatter.base import Field, Downgrade, Formatter

"""
    准备测试数据
"""


class TestFormatter(Formatter):
    FIELDS = [
        Field('name', converter=lambda name: 'Mr.' + name),
        Field('value', converter=lambda value: int(value), downgrade=Downgrade(0)),
        Field('count'),
    ]


class TestModel(object):
    def __init__(self, name=None, value=None, count=None):
        self.name = name
        self.value = value
        self.count = count


class TestModelB(object):
    pass


formatter_mappings = {
    TestModel: TestFormatter
}

"""end"""


class TestFormatter(TestCase):

    def test_register_formatter(self):
        Formatter.register_formatter(formatter_mappings)
        self.assertDictContainsSubset(formatter_mappings, Formatter._FORMATTER_MAPS)

    def test_get_formatter(self):
        Formatter.register_formatter(formatter_mappings)

        formatter = Formatter.get_formatter(TestModel)
        self.assertTrue(formatter is formatter_mappings[TestModel])

        formatter = Formatter.get_formatter(TestModel())
        self.assertTrue(formatter is formatter_mappings[TestModel])

        formatter = Formatter.get_formatter(TestModelB)
        self.assertTrue(formatter is None)

    def test_downgrade(self):
        # 测试降级
        Formatter.register_formatter(formatter_mappings)
        test_model = TestModel(name='He', value='10a', count=100)
        format_result = Formatter.format(test_model)
        self.assertDictEqual(format_result, {
            'name': 'Mr.He',
            'value': 0,
            'count': 100
        })

    def test_field(self):
        with self.assertRaises(DowngradeException):
            Field(name='hi', downgrade=0)

    def test_format(self):
        Formatter.register_formatter(formatter_mappings)

        test_model = TestModel(name='He', value='10', count=100)
        format_result = Formatter.format(test_model)
        self.assertDictEqual(format_result, {
            'name': 'Mr.He',
            'value': 10,
            'count': 100
        })

        # 测试 list format
        test_models = [TestModel(name='He', value='10', count=100),
                       TestModel(name='Wei', value='20', count=1)]
        format_result = Formatter.format(test_models)
        self.assertDictEqual(format_result[0], {
            'name': 'Mr.He',
            'value': 10,
            'count': 100
        })
        self.assertDictEqual(format_result[1], {
            'name': 'Mr.Wei',
            'value': 20,
            'count': 1
        })

        # 测试嵌套 format
        test_models = TestModel(name='He', value='10', count=TestModel(name='child', value='20', count=1))
        format_result = Formatter.format(test_models)
        self.assertDictEqual(format_result, {
            'name': 'Mr.He',
            'value': 10,
            'count': {
                'name': 'Mr.child',
                'value': 20,
                'count': 1,
            }
        })
