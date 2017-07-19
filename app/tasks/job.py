# coding=utf-8
import logging
from math import ceil

import requests
from lxml import etree
from retrying import retry
from requests.exceptions import RequestException

from common import constants
from app.tasks import celery_app
from app.controllers.job import JobController
from app.controllers.city import CityController
from app.controllers.keyword import KeywordController
from app.controllers.job_keyword import JobKeywordController
from app.utils.time_tools import job_date2timestamp
from app.utils.util import crawler_sleep
from app.utils.cookies import Cookies
from common.exception import RequestsError
from common.constants import EDUCATION_REQUEST_DICT, JOB_NATURE_DICT, WORK_YEARS_REQUEST_DICT
from app.utils.http_tools import generate_http_header, filter_http_tag

logger = logging.getLogger(__name__)


@celery_app.task(ignore_result=True)
def update_job_data(company_id):
    """更新职位数据"""
    response = request_job_json(company_id=company_id, page_no=1)
    # 计算该公司职位的页数
    page_count = int(ceil(
        int(response['content']['data']['page']['totalCount']) / int(response['content']['data']['page']['pageSize'])))
    for page_no in range(1, page_count + 1):
        json_result = request_job_json(company_id=company_id, page_no=page_no)
        jobs = json_result['content']['data']['page']['result']
        for job in jobs:
            job_id = job['positionId']
            if JobController.count(id=int(job_id)) == 0:
                generate_job_data(job, company_id)


def generate_job_data(job, company_id):
    """生成职位数据"""
    department, description, keywords = requests_job_detail_data(job['positionId'])
    job_id = job['positionId']
    city_id = 0 if 'city' not in job else CityController.get_city_id_by_name(job['city'])
    title = job['positionName']
    work_year = filter_http_tag(job['workYear'])
    if work_year not in WORK_YEARS_REQUEST_DICT:
        logger.error(work_year + 'not in WORK_YEAR_DICT')
    work_year = WORK_YEARS_REQUEST_DICT[work_year] if work_year in WORK_YEARS_REQUEST_DICT else WORK_YEARS_REQUEST_DICT['unknown']
    salary = job['salary']
    education = EDUCATION_REQUEST_DICT[job['education']]
    department = department
    description = description
    advantage = job['positionAdvantage'] if 'positionAdvantage' in job else ''
    job_nature = JOB_NATURE_DICT[job['jobNature']]
    created_at = job_date2timestamp(job['createTime'])

    JobController.add(
        id=job_id,
        company_id=company_id,
        title=title,
        work_year=work_year,
        city_id=city_id,
        salary=salary,
        education=education,
        department=department,
        description=description,
        advantage=advantage,
        job_nature=job_nature,
        created_at=created_at
    )
    for keyword in keywords:
        keyword_id = KeywordController.get_keyword_id_by_name(keyword)
        JobKeywordController.add(job_id, keyword_id, city_id)


@retry(stop_max_attempt_number=constants.RETRY_TIMES, stop_max_delay=constants.STOP_MAX_DELAY,
       wait_fixed=constants.WAIT_FIXED)
def requests_job_detail_data(job_id):
    """请求职位详情页数据"""
    headers = generate_http_header()
    crawler_sleep()
    try:
        response = requests.get(
            url=constants.JOB_DETAIL_URL.format(job_id=job_id),
            headers=headers,
            cookies=Cookies.get_random_cookies(),
            allow_redirects=False,
            timeout=constants.TIMEOUT)
    except RequestException as e:
        logging.error(e)
        raise RequestsError(error_log=e)
    html = etree.HTML(response.text)
    department = html.xpath('//div[@class="job-name"]/div[@class="company"]/text()')
    description = html.xpath('//dd[@class="job_bt"]/div//text()')
    keywords = html.xpath('//dd[@class="job_request"]//li[@class="labels"]/text()')
    return format_tag(department, description, keywords, job_id)


def format_tag(department, description, keywords, job_id=None):
    if len(keywords) == 0:
        logger.error('keywords is None, job id is {}'.format(job_id))
        keywords = []
    else:
        keywords = set(map(filter_http_tag, keywords))
        keywords = set(map(lambda item: item.lower(), keywords))

    if len(description) == 0:
        logger.warning('description is None, job id is {}'.format(job_id))
        description = ''
    else:
        description = ' '.join(map(filter_http_tag, description))

    if len(department) == 0:
        logger.error('department is None or error format, job id is {}'.format(job_id))
        department = ''
    else:
        department = filter_http_tag(department[0])
    return department, description, keywords


@retry(stop_max_attempt_number=constants.RETRY_TIMES, stop_max_delay=constants.STOP_MAX_DELAY,
       wait_fixed=constants.WAIT_FIXED)
def request_job_json(company_id, page_no):
    prams = {
        'companyId': company_id,
        'positionFirstType': u"技术",
        'pageNo': page_no,
        'pageSize': 10,
    }
    headers = generate_http_header()
    crawler_sleep()
    try:
        cookies = Cookies.get_random_cookies()
        response_json = requests.get(
            url=constants.COMPANY_JOB_URL,
            params=prams,
            headers=headers,
            cookies=cookies,
            timeout=constants.TIMEOUT).json()
        if 'content' not in response_json:
            Cookies.remove_cookies(cookies)
            raise RequestsError(error_log='wrong response content')
    except RequestException as e:
        logging.error(e)
        raise RequestsError(error_log=e)
    return response_json
