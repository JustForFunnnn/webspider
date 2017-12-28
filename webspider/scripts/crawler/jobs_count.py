# coding=utf-8
from __future__ import absolute_import
import logging

import requests
from retrying import retry
from requests.exceptions import RequestException

from webspider.tasks import celery_app
from common import constants
from common.exception import RequestsError
from webspider.controllers.keyword import KeywordController
from webspider.controllers.job_quantity import JobsCountController
from webspider.utils.util import crawler_sleep
from webspider.utils.cookies import Cookies
from webspider.utils.http_tools import generate_http_header
from webspider.utils.time_tools import get_date_begin_by_timestamp
from webspider.controllers.job import get_jobs_statistics
from webspider.utils.cache import cache_clear


@celery_app.task()
def crawl_lagou_job_quantity():
    pre_date = get_date_begin_by_timestamp(after_days=-1)
    keywords = KeywordController.get_most_frequently_keywords(limit=2000)
    logging.info('{} crawl_lagou_job_count 定时任务运行中! 关键词 {} 个'.format(pre_date, len(keywords)))
    for keyword in keywords:
        city_job_quantity = {
            '全国': 0, '北京': 0, '上海': 0, '广州': 0, '深圳': 0, '杭州': 0, '成都': 0
        }
        for city in city_job_quantity:
            response_json = request_job_quantity_json(city=city, keyword=keyword)
            try:
                city_job_quantity[city] = response_json['content']['positionResult']['totalCount']
            except Exception:
                logging.getLogger(__name__).error('获取 jobs count 信息失败, 关键词为 {}'.format(keyword.name), exc_info=True)
        JobsCountController.add(date=pre_date, keyword_id=keyword.id,
                                all_city=city_job_quantity['全国'], beijing=city_job_quantity['北京'],
                                shanghai=city_job_quantity['上海'], guangzhou=city_job_quantity['广州'],
                                shenzhen=city_job_quantity['深圳'], hangzhou=city_job_quantity['杭州'],
                                chengdu=city_job_quantity['成都'])
    logging.info('crawl_lagou_job_count 任务完成!')
    # 失效缓存
    remove_count = cache_clear(get_jobs_statistics)
    logging.info('主动失效缓存成功, 数量{}'.format(remove_count))


@retry(stop_max_attempt_number=constants.RETRY_TIMES, stop_max_delay=constants.STOP_MAX_DELAY,
       wait_fixed=constants.WAIT_FIXED)
def request_job_quantity_json(city, keyword):
    query_string = {'needAddtionalResult': False}
    if city != '全国':
        query_string['city'] = city
    form_data = {
        'first': False,
        'pn': 1,
        'kd': keyword.name
    }
    headers = generate_http_header(is_crawl_job_quantity=True)
    crawler_sleep()
    try:
        cookies = Cookies.get_random_cookies()
        response = requests.post(url=constants.JOB_JSON_URL,
                                 params=query_string,
                                 data=form_data,
                                 headers=headers,
                                 cookies=cookies,
                                 allow_redirects=False,
                                 timeout=constants.TIMEOUT)
        response_json = response.json()
        if 'content' not in response_json:
            Cookies.remove_cookies(cookies)
            raise RequestsError(error_log='wrong response content')
    except RequestException as e:
        logging.error(e)
        raise RequestsError(error_log=e)
    return response_json
