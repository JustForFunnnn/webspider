# coding=utf-8
import re
import random
import logging

import requests
from lxml import etree

from webspider import constants


def filter_http_tag(string):
    """过滤网页端的多余字符和标签"""
    pattern = r'<br/?>|\n'
    replace_char = ''
    string = re.sub(pattern=pattern, repl=replace_char, string=string)
    return string.strip()


def generate_http_request_headers(referer=None):
    """构造 HTTP 请求头"""
    header = constants.HTTP_HEADER
    header['User-Agent'] = random.choice(constants.USER_AGENT_LIST)
    if referer:
        header['Referer'] = referer
    return header


def filter_unavailable_proxy(proxy_list, proxy_type='HTTPS'):
    """过滤掉无用的代理"""
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
        except Exception:
            pass
    return available_proxy_list


def get_proxys(pages=4):
    """获取代理"""
    proxy_list = []
    url = 'http://www.xicidaili.com/wn/'
    headers = generate_http_header()
    headers.update(
        {
            'Referer': 'http://www.xicidaili.com/wn/',
            'Host': 'www.xicidaili.com',
        }
    )
    for page_no in range(1, pages + 1):
        response = requests.get(url=url.format(page_no=page_no), headers=headers)
        html = etree.HTML(response.text)
        ips = html.xpath("//table[@id='ip_list']/tr/td[2]/text()")
        ports = html.xpath("//table[@id='ip_list']/tr/td[3]/text()")
        assert len(ips) == len(ports)
        for (ip, port) in zip(ips, ports):
            proxy_list.append(constants.HTTP_PROXY_FORMATTER.format(ip=ip, port=port))
    return proxy_list
