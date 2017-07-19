# coding=utf-8
import time
import random
import logging
from functools import lru_cache

import requests

from common import constants
from app.model.city import CityModel
from app.utils.http_tools import generate_http_header

logger = logging.getLogger(__name__)


class CityController(object):
    @classmethod
    def get_all_city_company_count(cls):
        """
        获取所有拉勾上的城市 的公司数目
        :return: {'city_id': total_company_count, ....}
        """
        citys = CityModel.list()
        city_company_counts_dict = {}
        for city in citys:
            headers = generate_http_header()
            # proxies = {"https": redis_instance.srandmember(constants.REDIS_PROXY_KEY).decode()}
            url = constants.CITY_COMPANY_URL.format(city=city.id, finance_stage=0, industry=0)
            prams = {
                'first': False,
                'pn': 1,
                'sortField': 1,
                'havemark': 0,
            }
            response = requests.get(url=url, params=prams, headers=headers,
                                    timeout=constants.TIMEOUT).json()
            city_company_counts_dict[city.id] = int(response['totalCount'])
            time.sleep(constants.MIN_SLEEP_TIME)
        return city_company_counts_dict

    @classmethod
    @lru_cache(maxsize=128)
    def get_city_id_by_name(cls, name):
        city = CityModel.get(name=name)
        return city.id if city else 0

    @classmethod
    def add(cls, id, name):
        CityModel.add(id=id, name=name)
        cls.get_city_id_by_name.cache_clear()
        cls.get_city_name_dict.cache_clear()

    @classmethod
    def list(cls):
        return CityModel.list()

    @classmethod
    @lru_cache(maxsize=1)
    def get_city_name_dict(cls):
        citys = CityModel.list()
        city_name_dict = {city.id: city.name for city in citys}
        city_name_dict[0] = 'unknown'
        return city_name_dict
