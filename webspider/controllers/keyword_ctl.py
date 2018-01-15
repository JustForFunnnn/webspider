# coding=utf-8
from tornado.escape import to_unicode

from webspider.models.keyword import KeywordModel


def insert_keyword_if_not_exist(name):
    sql = """INSERT INTO keyword(name)
SELECT :name AS name FROM dual
WHERE NOT EXISTS
(SELECT 1 FROM keyword WHERE name = :name)"""
    KeywordModel.execute_sql_string(sql_string=sql, parameters_dict={'name': to_unicode(name)})


def get_keyword_id_by_name(name):
    keyword = KeywordModel.get_one(filter_by={'name': name})
    if not keyword:
        raise ValueError('Get None when keyword name is {}'.format(name))
    return keyword.id
