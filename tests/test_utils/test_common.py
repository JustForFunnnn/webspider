# coding=utf-8
from unittest import TestCase

from webspider.utils.common import get_key_from_dict_by_value, get_field_statistics


class TestUtilCommon(TestCase):
    def test_get_key_from_dict_by_value(self):
        dictionary = {
            '全国': 1,
            '北京': 2,
            '广州': 3,
        }
        key = get_key_from_dict_by_value(1, dictionary)
        self.assertEqual(key, '全国')

        # no key
        with self.assertRaises(ValueError):
            get_key_from_dict_by_value(4, dictionary)

        dictionary = {
            '全国': 1,
            '北京': 1,
            '广州': 3,
        }
        key = get_key_from_dict_by_value(3, dictionary)
        self.assertEqual(key, '广州')
        # multi key
        with self.assertRaises(AttributeError):
            get_key_from_dict_by_value(1, dictionary)

    def test_get_field_statistics(self):
        statistics = get_field_statistics([0, 0, 0, 1, 1], {'男': 0, '女': 1, '不明': 2})
        self.assertDictEqual(statistics, {'男': 3, '女': 2})
