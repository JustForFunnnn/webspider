# coding=utf-8
import re
import random
import logging

import requests
from lxml import etree

from common import constants
from common.db import redis_instance


def crawl_proxy():
    # 获取代理
    if redis_instance.get('crawling_proxy') == b'1':
        return
    redis_instance.set('crawling_proxy', 1)
    proxy_list = get_proxy_list()
    redis_instance.sadd(constants.REDIS_PROXY_KEY, *proxy_list)
    redis_instance.set('crawling_proxy', 0)


def filter_http_tag(string):
    """
    过滤网页端的多余字符和标签
    :param string:
    :return:
    """
    pattern = r'<br/?>|\n'
    replace_char = ''
    string = re.sub(pattern=pattern, repl=replace_char, string=string)
    return string.strip()


def generate_http_header():
    """
    构造 HTTP 请求头
    :return:
    """
    header = constants.HTTP_HEADER
    header['User-Agent'] = random.choice(constants.USER_AGENT_LIST)
    return header


def get_proxy_list(proxy_type='HTTPS'):
    if proxy_type == 'HTTPS':
        proxy_list = get_proxy_list_from_66ip()
    else:
        proxy_list = get_proxy_list_from_kuaidaili()
    return proxy_list


def filter_unavailable_proxy(proxy_list, proxy_type='HTTPS'):
    """
    过滤掉无用的代理
    :param proxy_list: 全部代理列表
    :param proxy_type: 
    :return: 可用的代理列表
    """
    available_proxy_list = []
    for proxy in proxy_list:
        if proxy_type == 'HTTPS':
            protocol = 'https'
        else:
            protocol = 'http'
        try:
            response = requests.get('https://www.lagou.com/gongsi/0-0-0.json',
                                    proxies={protocol: proxy},
                                    timeout=3)
            if response.status_code == constants.HTTP_SUCCESS and 'totalCount' in response.json():
                available_proxy_list.append(proxy)
                logging.info('可用代理数量 {}'.format(len(available_proxy_list)))
        except:
            pass
    return available_proxy_list


def get_proxy_list_from_66ip():
    """
    获取代理
    :return:
    """
    proxy_list = []
    url = 'http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=0&proxytype=1&api=66ip'
    response = requests.get(url=url)
    ip_ports = re.findall(pattern=r'(\d+.\d+.\d+.\d+:\d+)', string=response.text)
    for ip_port in ip_ports:
        proxy_list.append('http://' + ip_port)
    return filter_unavailable_proxy(proxy_list=proxy_list)


def get_proxy_list_from_kuaidaili():
    """
    获取代理
    :return:
    """
    proxy_list = []
    url = 'http://www.kuaidaili.com/free/inha/{page_no}/'
    for page_no in range(1, 15):
        html = etree.HTML(requests.get(url=url.format(page_no=page_no)).text)
        tr_list = html.xpath("//tbody/tr")
        for tr in tr_list[1:-1]:
            res = tr.xpath('./td/text()')
            ip, port = res[0].replace('\r\n', '').replace(' ', ''), res[1].replace('\r\n', '').replace(' ', '')
            proxy_list.append(constants.HTTP_PROXY_FORMATTER.format(ip=ip, port=port))
    return filter_unavailable_proxy(proxy_list=proxy_list)
