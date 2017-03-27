# coding=utf-8
from tests import BaseTestCase
from app.model.keyword import KeywordModel


class KeywordModelTestCase(BaseTestCase):
    def test_get_keyword(self):
        keyword = KeywordModel.get(name='python')
        self.assertEqual(keyword.id, 100)
        self.assertEqual(keyword.name, 'python')

    def test_list_keyword(self):
        keywords = KeywordModel.list()
        self.assertEqual(len(keywords), 2)
        keywords = KeywordModel.list(name='ja')
        self.assertEqual(len(keywords), 1)
        self.assertEqual(keywords[0].id, 101)

    def test_insert_if_not_exist_keyword(self):
        data = {
            'name': '吃饭',
        }
        KeywordModel.insert_if_not_exist(**data)
        keywords = KeywordModel.list()
        self.assertEqual(len(keywords), 3)
        keyword = KeywordModel.get(name='吃饭')
        self.assertEqual(keyword.id, 102)
        self.assertEqual(keyword.name, '吃饭')

        KeywordModel.insert_if_not_exist(name='java')
        KeywordModel.insert_if_not_exist(name='python')
        keywords = KeywordModel.list()
        self.assertEqual(len(keywords), 3)
