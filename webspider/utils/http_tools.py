# coding=utf-8
import re
import time
import random
import logging

import requests
from lxml import etree
from retrying import retry

from webspider import constants


def to_plaintext(content, pattern=r'<br/?>|\n', strip=True):
    """
    根据 pattern 过滤文本
    :param content: 需要过滤的文本
    :param pattern: 需要过滤内容的正则表达式
    :param strip: 是否去掉首尾空格
    :return:
    """
    plaintext = re.sub(pattern=pattern, repl=pattern, string=content)
    if strip:
        plaintext.strip()
    return plaintext


def generate_http_request_headers(referer=None):
    """构造 HTTP 请求头"""
    header = constants.HTTP_HEADER
    header['User-Agent'] = random.choice(constants.USER_AGENT_LIST)
    if referer:
        header['Referer'] = referer
    return header


@retry(stop_max_attempt_number=constants.RETRY_TIMES, stop_max_delay=constants.STOP_MAX_DELAY,
       wait_fixed=constants.WAIT_FIXED)
def requests_get(url, params=None, headers=None, allow_redirects=False, timeout=constants.TIMEOUT, need_sleep=True,
                 **kwargs):
    if need_sleep:
        time.sleep(random.randint(constants.MIN_SLEEP_SECS, constants.MAX_SLEEP_SECS))
    if not headers:
        headers = generate_http_request_headers()
    return requests.get(url=url, params=params, headers=headers, allow_redirects=allow_redirects,
                        timeout=timeout, **kwargs)


@retry(stop_max_attempt_number=constants.RETRY_TIMES, stop_max_delay=constants.STOP_MAX_DELAY,
       wait_fixed=constants.WAIT_FIXED)
def requests_post(url, data=None, params=None, headers=None, allow_redirects=False, timeout=constants.TIMEOUT,
                  need_sleep=True, **kwargs):
    if need_sleep:
        time.sleep(random.randint(constants.MIN_SLEEP_SECS, constants.MAX_SLEEP_SECS))
    if not headers:
        headers = generate_http_request_headers()
    return requests.post(url=url, data=data, params=params, headers=headers, allow_redirects=allow_redirects,
                         timeout=timeout, **kwargs)


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
