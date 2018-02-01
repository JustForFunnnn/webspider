# coding=utf-8
import time
import random

import requests
from retrying import retry

from webspider import constants


def generate_http_request_headers(referer=None):
    """构造 HTTP 请求头"""
    header = constants.HTTP_HEADER
    header['User-Agent'] = random.choice(constants.USER_AGENT_LIST)
    if referer:
        header['Referer'] = referer
    return header


@retry(stop_max_attempt_number=constants.RETRY_TIMES, stop_max_delay=constants.STOP_MAX_DELAY,
       wait_fixed=constants.WAIT_FIXED)
def requests_get(url, params=None, headers=None, allow_redirects=False, timeout=constants.REQUEST_TIMEOUT,
                 need_sleep=True, **kwargs):
    if need_sleep:
        time.sleep(random.randint(constants.MIN_SLEEP_SECS, constants.MAX_SLEEP_SECS))
    if not headers:
        headers = generate_http_request_headers()
    return requests.get(url=url, params=params, headers=headers, allow_redirects=allow_redirects,
                        timeout=timeout, **kwargs)


@retry(stop_max_attempt_number=constants.RETRY_TIMES, stop_max_delay=constants.STOP_MAX_DELAY,
       wait_fixed=constants.WAIT_FIXED)
def requests_post(url, data=None, params=None, headers=None, allow_redirects=False, timeout=constants.REQUEST_TIMEOUT,
                  need_sleep=True, **kwargs):
    if need_sleep:
        time.sleep(random.randint(constants.MIN_SLEEP_SECS, constants.MAX_SLEEP_SECS))
    if not headers:
        headers = generate_http_request_headers()
    return requests.post(url=url, data=data, params=params, headers=headers, allow_redirects=allow_redirects,
                         timeout=timeout, **kwargs)
