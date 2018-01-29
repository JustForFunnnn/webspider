# coding=utf-8

from sqlalchemy.exc import IntegrityError

from webspider.models.city import CityModel


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
