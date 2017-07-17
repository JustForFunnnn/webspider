# coding=utf-8
from __future__ import absolute_import
import logging

import requests
from retrying import retry
from requests.exceptions import RequestException

from . import celery_app
from common import constants
from common.exception import RequestsError
from app.controllers.keyword import KeywordController
from app.controllers.jobs_count import JobsCountController
from app.utils.util import crawler_sleep
from app.utils.http_tools import generate_http_header
from app.utils.time_tools import get_date_begin_by_timestamp


@celery_app.task
def crawl_lagou_jobs_count():
    pre_date = get_date_begin_by_timestamp(after_days=-1)
    keywords = KeywordController.get_most_frequently_keywords(limit=400)
    logging.info('{} crawl_lagou_job_count 定时任务运行中! 关键词 {} 个'.format(pre_date, len(keywords)))
    for keyword in keywords:
        city_jobs_count = {
            '全国': 0, '北京': 0, '上海': 0, '广州': 0, '深圳': 0, '杭州': 0, '成都': 0
        }
        for city in city_jobs_count:
            response_json = request_jobs_count_json(city=city, keyword=keyword)
            city_jobs_count[city] = response_json['content']['positionResult']['totalCount']
        JobsCountController.add(date=pre_date, keyword_id=keyword.id,
                                all_city=city_jobs_count['全国'], beijing=city_jobs_count['北京'],
                                shanghai=city_jobs_count['上海'], guangzhou=city_jobs_count['广州'],
                                shenzhen=city_jobs_count['深圳'], hangzhou=city_jobs_count['杭州'],
                                chengdu=city_jobs_count['成都'])
    logging.info('crawl_lagou_job_count 任务完成!')


@retry(stop_max_attempt_number=constants.RETRY_TIMES, stop_max_delay=constants.STOP_MAX_DELAY,
       wait_fixed=constants.WAIT_FIXED)
def request_jobs_count_json(city, keyword):
    query_string = {'needAddtionalResult': False}
    if city != '全国':
        query_string['city'] = city
    form_data = {
        'first': False,
        'pn': 1,
        'kd': keyword.name
    }
    headers = generate_http_header(is_crawl_jobs_count=True)
    crawler_sleep()
    try:
        response = requests.post(url=constants.JOB_JSON_URL,
                                 params=query_string,
                                 data=form_data,
                                 headers=headers,
                                 timeout=constants.TIMEOUT)
        response_json = response.json()
    except RequestException as e:
        logging.error(e)
        raise RequestsError(error_log=e)
    return response_json
