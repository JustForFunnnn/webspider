# coding=utf-8
import re
import random
import logging

import requests
from lxml import etree

from common import constants
from common.db import redis_instance


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


def generate_http_header(is_crawl_jobs_count=False):
    """
    构造 HTTP 请求头
    :return:
    """
    header = constants.HTTP_HEADER
    header['User-Agent'] = random.choice(constants.USER_AGENT_LIST)
    # lagou 会针对访问的不同链接 检测header 的referer
    if is_crawl_jobs_count:
        header['Referer'] = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
    return header


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
                                    timeout=1)
            if response.status_code == constants.HTTP_SUCCESS and 'totalCount' in response.json():
                available_proxy_list.append(proxy)
                logging.info('可用代理数量 {}'.format(len(available_proxy_list)))
        except:
            pass
    return available_proxy_list


def get_proxys(numbers=200):
    """获取代理"""
    proxy_list = []
    url = 'http://www.66ip.cn/nmtq.php?getnum={numbers}&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=0&proxytype=1&api=66ip'.format(
        numbers=numbers)
    response = requests.get(url=url)
    ip_ports = re.findall(pattern=r'(\d+.\d+.\d+.\d+:\d+)', string=response.text)
    for ip_port in ip_ports:
        proxy_list.append('http://' + ip_port)
    return proxy_list
