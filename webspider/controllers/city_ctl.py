# coding=utf-8
import logging

from webspider.models.city import CityModel

logger = logging.getLogger(__name__)


def get_city_id_by_name(name):
    city = CityModel.get_one(filter_by={'name': name})
    if not city:
        raise ValueError('Get None when city name is {}'.format(name))
    return city.id

    # @classmethod
    # @lru_cache(maxsize=128)
    # def get_city_id_by_name(cls, name):
    #     city = CityModel.get(name=name)
    #     return city.id if city else 0
    #
    # @classmethod
    # def add(cls, id, name):
    #     CityModel.add(id=id, name=name)
    #     cls.get_city_id_by_name.cache_clear()
    #     cls.get_city_name_dict.cache_clear()
    #
    # @classmethod
    # def list(cls):
    #     return CityModel.list()
    #
    # @classmethod
    # @lru_cache(maxsize=1)
    # def get_city_name_dict(cls):
    #     citys = CityModel.list()
    #     city_name_dict = {city.id: city.name for city in citys}
    #     city_name_dict[0] = 'unknown'
    #     return city_name_dict
