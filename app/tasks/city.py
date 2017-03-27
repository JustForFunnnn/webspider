# coding=utf-8
import re
import logging

import requests
from lxml import etree

from common import constants
from app.controllers.city import CityController

logger = logging.getLogger(__name__)


def update_city_data():
    """
    获取拉勾上所有城市的信息 并更新数据库相关表的信息
    :return:
    """
    html = etree.HTML(requests.get(constants.ALL_CITY_URL).text)
    a_list = html.xpath("//ul[@class='city_list']/li/a")
    for a in a_list:
        city_name = a.xpath('./text()')[0]
        city_id = a.xpath('./@href')[0]
        city_id = re.findall(pattern=r'/(\d+)-\d+-\d+', string=city_id)[0]
        CityController.add(id=city_id, name=city_name)
