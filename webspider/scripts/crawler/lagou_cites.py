# coding=utf-8
import re
import logging

import requests
from lxml import etree

from webspider import constants
from webspider.models.city import CityModel

logger = logging.getLogger(__name__)


def crawl_lagou_cites():
    """
    获取拉勾上所有城市的信息
    :return [models.city.CityModel instances, .....]
    """
    logger.info(u'begin crawl cities info......')
    html = etree.HTML(requests.get(constants.ALL_CITY_URL).text)
    cities_html_list = html.xpath("//ul[@class='city_list']/li/a")
    cities = []
    for city_html in cities_html_list:
        city_name = city_html.xpath('./text()')[0]
        city_id = re.findall(pattern=r'/(\d+)-\d+-\d+', string=city_html.xpath('./@href')[0])[0]
        cities.append(CityModel(id=city_id, name=city_name))

    # TODO remove
    if cities:
        CityModel.session.bulk_save_objects(cities)

    logger.info(u'crawl cities info finished! cites quantity is {cities_count}'.format(cities_count=len(cities)))
    return cities
