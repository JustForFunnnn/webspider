# coding=utf-8
import re
import logging

import requests
from lxml import etree
from tornado.util import ObjectDict

from webspider import constants

logger = logging.getLogger(__name__)


def crawl_lagou_cites():
    """
    获取拉勾上所有城市的信息
    :return [
        {
            'id': 111,
            'name': '广州'
        },
        .....
    ]
    """
    logger.info(u'begin crawl cities info......')

    response_html = etree.HTML(requests.get(constants.ALL_CITY_URL).text)
    cities_html_list = response_html.xpath("//ul[@class='city_list']/li/a")

    cities_dicts = []
    for city_html in cities_html_list:
        city_name = city_html.xpath('./text()')[0]
        city_id = re.findall(pattern=r'/(\d+)-\d+-\d+', string=city_html.xpath('./@href')[0])[0]
        cities_dicts.append(ObjectDict(id=city_id, name=city_name))

    logger.info(u'crawl cities info finished! cites quantity is {cities_count}'.format(cities_count=len(cities_dicts)))
    return cities_dicts
