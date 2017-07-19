# coding=utf-8
import time
import random
import logging
import requests

from common import constants
from app.utils.http_tools import get_proxys


class Cookies(object):
    _cookies = []
    _last_update_time = None

    @classmethod
    def refresh_cookies(cls):
        """刷新 cookie """
        proxys = get_proxys(400)
        cls._cookies = cls.get_lagou_cookies_from_proxys(proxys)
        cls._last_update_time = time.time()

    @classmethod
    def get_random_cookies(cls):
        now = time.time()
        if len(cls._cookies) == 0 or (now - cls._last_update_time) >= constants.SECONDS_OF_DAY:
            cls.refresh_cookies()
        return random.choice(cls._cookies)

    @classmethod
    def remove_cookies(cls, cookies):
        cls._cookies.remove(cookies)

    @classmethod
    def get_lagou_cookies_from_proxys(cls, proxys, proxy_type='https'):
        cookies = []
        for proxy in proxys:
            try:
                response = requests.get('https://www.lagou.com/',
                                        proxies={proxy_type: proxy},
                                        timeout=2)
                if response.status_code == constants.HTTP_SUCCESS and len(response.cookies):
                    cookies.append(response.cookies)
            except:
                pass
        logging.info('可用cookies数量 {}'.format(len(cookies)))
        return cookies
