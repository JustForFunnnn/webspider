# coding=utf-8

from tornado.escape import to_unicode

from webspider.models.city import CityModel


def get_city_id_by_name(name):
    city = CityModel.get_one(filter_by={'name': name})
    if not city:
        raise ValueError('Get None when city name is {}'.format(name))
    return city.id


def insert_city_if_not_exist(name):
    sql = """INSERT INTO city(name)
SELECT :name AS name FROM dual
WHERE NOT EXISTS
(SELECT 1 FROM city WHERE name = :name)"""
    CityModel.execute_sql_string(sql_string=sql, parameters_dict={'name': to_unicode(name)})
