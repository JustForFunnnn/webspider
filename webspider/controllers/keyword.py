# coding=utf-8
from webspider.model.keyword import KeywordModel


class KeywordController(object):
    @classmethod
    def get(cls, name):
        return KeywordModel.get(name=name)

    @classmethod
    def get_keyword_id_by_name(cls, name):
        KeywordModel.insert_if_not_exist(name=name)
        keyword = KeywordModel.get(name=name)
        return keyword.id

    @classmethod
    def get_most_frequently_keywords(cls, limit=10):
        return KeywordModel.get_most_frequently_keywords(limit=limit)
