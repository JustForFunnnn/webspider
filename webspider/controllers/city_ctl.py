# coding=utf-8

from sqlalchemy.exc import IntegrityError

from webspider.models.city import CityModel
from webspider.utils.cache import simple_cache


def get_city_id_by_name(name):
    city = CityModel.get_one(filter_by={'name': name})
    if not city:
        raise ValueError('Get None when city name is {}'.format(name))
    return city.id


def insert_city_if_not_exist(name):
    if CityModel.is_exist(filter_by={'name': name}):
        return
    try:
        city_id = CityModel.add(name=name)
        return city_id
    except IntegrityError:
        pass


@simple_cache(ex=60 * 60 * 1)
def get_city_name_dict():
    """
    :return: dict eg: {'北京': 2, '上海':3, ......}
    """
    cities = CityModel.list()
    return {city.name: city.id for city in cities}
