# coding=utf-8
from webspider.models.industry import IndustryModel

from tornado.escape import to_unicode


def insert_industry_if_not_exist(name):
    sql = """INSERT INTO industry(name)
SELECT :name AS name FROM dual
WHERE NOT EXISTS
(SELECT 1 FROM industry WHERE name = :name)"""
    IndustryModel.execute_sql_string(sql_string=sql, parameters_dict={'name': to_unicode(name)})


def get_industry_id_by_name(name):
    industry = IndustryModel.get_one(filter_by={'name': name})
    if not industry:
        raise ValueError('Get None when industry name is {}'.format(name))
    return industry.id
