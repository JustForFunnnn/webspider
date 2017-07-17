# coding=utf-8
import re
import logging
from math import ceil

import requests
from lxml import etree
from retrying import retry
from requests.exceptions import RequestException

from common import constants
from common.db import redis_instance
from app.tasks import celery_app
from app.tasks.job import update_job_data
from common.exception import RequestsError
from app.controllers.company import CompanyController
from app.controllers.company_industry import CompanyIndustryController
from app.controllers.industry import IndustryController
from app.utils.http_tools import generate_http_header, filter_http_tag
from app.utils.util import crawler_sleep
from common.constants import FINANCE_STAGE_DICT, COMPANY_SIZE_DICT

logger = logging.getLogger(__name__)


@celery_app.task(ignore_result=True)
def update_company_data(city_id, finance_stage_id, industry_id, update_job=False):
    """更新公司数据"""
    logger.info('正在爬取城市={}, 融资类型={}, 行业类别={}'.format(city_id, finance_stage_id, industry_id))
    # 生成访问链接
    url = constants.CITY_COMPANY_URL.format(city=city_id, finance_stage=finance_stage_id, industry=industry_id)
    response = request_company_json(url, page_no=1)
    # 计算需要爬取的页数
    page_count = int(ceil(int(response['totalCount']) / int(response['pageSize'])))

    for page_no in range(1, page_count + 1):
        logger.info('正在爬取城市={}, 融资类型={}, 行业类别={}, 第 「{}」 页'.format(city_id, finance_stage_id, industry_id, page_no))
        response = request_company_json(url=url, page_no=page_no)
        companys = response['result']
        if len(companys) == 0:
            break
        for company in companys:
            company_id = int(company['companyId'])
            if CompanyController.count(id=company_id) == 0:
                generate_company_data(company=company, city_id=city_id)
            # 更新公司下职位的数据
            if update_job and not redis_instance.sismember(constants.REDIS_VISITED_COMPANY_KEY, company_id):
                redis_instance.sadd(constants.REDIS_VISITED_COMPANY_KEY, company_id)
                update_job_data(company_id=company_id)
    logger.info('爬取城市={}, 融资类型={}, 行业类别={}, 任务结束'.format(city_id, finance_stage_id, industry_id))


def generate_company_data(company, city_id):
    """生成公司数据"""
    company_id = company['companyId']
    shortname = filter_http_tag(company['companyShortName'])
    fullname = filter_http_tag(company['companyFullName'])
    finance_stage = filter_http_tag(company['financeStage']).upper()
    if finance_stage not in FINANCE_STAGE_DICT:
        logger.error(company['financeStage'] + 'not in FINANCE_STAGE_DICT')
    finance_stage = FINANCE_STAGE_DICT[finance_stage] \
        if finance_stage in FINANCE_STAGE_DICT else FINANCE_STAGE_DICT[finance_stage]
    process_rate = company['processRate'] if 'processRate' in company else -1
    features = filter_http_tag(company['companyFeatures'])
    advantage, address, size, introduce = requests_company_detail_data(company_id=company_id)

    CompanyController.add(
        id=company_id,
        shortname=shortname,
        fullname=fullname,
        finance_stage=finance_stage,
        process_rate=process_rate,
        city_id=city_id,
        features=features,
        advantage=advantage,
        address=address,
        size=size,
        introduce=introduce,
    )
    industry_fields = set(re.split(",|，|、", company['industryField']))
    for industry_field in industry_fields:
        industry_id = IndustryController.get_industry_id_by_name(industry_field)
        CompanyIndustryController.add(company_id, industry_id, city_id)


@retry(stop_max_attempt_number=constants.RETRY_TIMES, stop_max_delay=constants.STOP_MAX_DELAY,
       wait_fixed=constants.WAIT_FIXED)
def requests_company_detail_data(company_id):
    """请求公司详情页数据"""
    headers = generate_http_header()
    crawler_sleep()
    try:
        response = requests.get(
            url=constants.COMPANY_DETAIL_URL.format(company_id=company_id),
            headers=headers,
            allow_redirects=False,
            timeout=constants.TIMEOUT)
    except RequestException as e:
        logging.error(e)
        raise RequestsError(error_log=e)
    html = etree.HTML(response.text)
    advantage = html.xpath('//div[@id="tags_container"]//li/text()')
    size = html.xpath('//div[@id="basic_container"]//li[3]/span/text()')
    address = html.xpath('//p[@class="mlist_li_desc"]/text()')
    introduce = html.xpath('//span[@class="company_content"]//text()')

    return format_tag(advantage, address, size, introduce, company_id)


def format_tag(advantage, address, size, introduce, company_id=None):
    """格式化数据"""
    if len(advantage) == 0:
        logger.warning('advantage is None, company id is {}'.format(company_id))
        advantage = ''
    else:
        advantage = ','.join(map(filter_http_tag, advantage))

    if len(introduce) == 0:
        logger.warning('introduce is None, company id is {}'.format(company_id))
        introduce = ''
    else:
        introduce = '  '.join(map(filter_http_tag, introduce))

    if len(address) == 0:
        logger.warning('address is None, company id is {}'.format(company_id))
        address = ''
    else:
        address = filter_http_tag(address[0])

    if len(size) == 0 or size[0] not in COMPANY_SIZE_DICT:
        logger.error('size is None or error format, company id is {}'.format(company_id))
        size = 'unknown'
    else:
        size = filter_http_tag(size[0])

    return advantage, address, COMPANY_SIZE_DICT[size], introduce


@retry(stop_max_attempt_number=constants.RETRY_TIMES, stop_max_delay=constants.STOP_MAX_DELAY,
       wait_fixed=constants.WAIT_FIXED)
def request_company_json(url, page_no):
    prams = {
        'first': False,
        'pn': page_no,
        'sortField': 1,
        'havemark': 0,
    }
    headers = generate_http_header()
    crawler_sleep()
    try:
        response_json = requests.get(
            url=url,
            params=prams,
            headers=headers,
            allow_redirects=False,
            timeout=constants.TIMEOUT).json()
    except RequestException as e:
        logging.error(e)
        raise RequestsError(error_log=e)
    return response_json
