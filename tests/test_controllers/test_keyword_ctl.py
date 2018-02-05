# coding=utf-8
from tests import BaseTestCase
from webspider.controllers import keyword_ctl
from webspider.models import KeywordModel


class TestKeywordController(BaseTestCase):
    def test_get_keyword_name_by_id(self):
        keyword_name = keyword_ctl.get_keyword_name_by_id(keyword_id=100)
        self.assertEqual(keyword_name, 'python')

        with self.assertRaises(ValueError):
            keyword_ctl.get_keyword_name_by_id(keyword_id=10001)

    def test_insert_keyword_if_not_exist(self):
        keyword_name = 'C--'
        keyword_id = keyword_ctl.insert_keyword_if_not_exist(keyword_name)
        self.assertTrue(keyword_id > 0)
        keyword = KeywordModel.get_by_pk(pk=keyword_id)
        self.assertEqual(keyword.name, keyword_name)

        self.assertIsNone(keyword_ctl.insert_keyword_if_not_exist(keyword_name))
