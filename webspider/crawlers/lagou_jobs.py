# coding=utf-8
import logging

from lxml import etree
from tornado.util import ObjectDict

from webspider import utils
from webspider import constants

logger = logging.getLogger(__name__)


def get_jobs_pagination_from_lg(lg_company_id, job_type, page_no=1, is_school_job=False):
    """
    爬取职位分页数据

    :param lg_company_id: 接口使用的公司 id
    :param job_type: 职位类型
    :param page_no: 页码
    :param is_school_job: 是否爬取校招职位
    :return:
    """
    params = {
        'companyId': lg_company_id,
        'positionFirstType': job_type,
        'schoolJob': is_school_job,
        'pageNo': page_no,
        'pageSize': 10,
    }
    response_json = utils.http_tools.requests_get(
        url=constants.COMPANY_JOBS_URL, params=params).json()
    pagination = utils.pagination.Pagination(per_page=int(response_json['content']['data']['page']['pageSize']),
                                             total=int(response_json['content']['data']['page']['totalCount']))

    return pagination


def get_jobs_from_lg(lg_company_id, job_type, page_no=1, is_school_job=False):
    """
    爬取职位数据

    返回的 dict 组成:
    lg_job_id:
        type: int
        meaning: 接口使用的职位 id
        eg: 1
    city_name:
        type: str
        meaning: 城市名
        eg: 北京
    title:
        type: str
        meaning: 职位标题
        eg: 招聘后端工程师
    salary:
        type: str
        meaning: 薪酬范围
        eg:  '10k~20k'
    education:
        type: str
        meaning: 教育背景要求
        eg: 本科或以上
    nature:
        type: str
        meaning: 职位性质
        eg: 全职
    work_year:
        type: str
        meaning: 工作年限要求
        eg:  1~3年
    advantage:
        type: str
        meaning: 职位优势
        eg:  大平台，五险一金
    department:
        type: str
        meaning: 招聘部门
        eg:  商业部
    keywords:
        type: List[str]
        meaning: 职位关键词
        eg: ['后端', 'Web', 'Python']
    description:
        type: List[str]
        meaning: 职位介绍
        eg: ['职位要求:', 'blablabla', '.......']

    :param lg_company_id: 接口使用的公司 id
    :param job_type: 职位类型
    :param page_no: 页码
    :param is_school_job: 是否爬取校招职位
    :param skip_exist: 是否跳过数据库已经存在的职位数据
    :return: 职位数据集合
    :rtype: List[tornado.util.ObjectDict]
    """
    params = {
        'companyId': lg_company_id,
        'positionFirstType': job_type,
        'schoolJob': is_school_job,
        'pageNo': page_no,
        'pageSize': 10,
    }
    response_json = utils.http_tools.requests_get(
        url=constants.COMPANY_JOBS_URL, params=params).json()
    jobs = response_json['content']['data']['page']['result']

    jobs_dicts = []
    for job in jobs:
        lg_job_id = job['positionId']
        job_detail = get_job_detail_from_lg(lg_job_id=lg_job_id)
        jobs_dicts.append(ObjectDict(
            lg_job_id=lg_job_id,
            city_name=job.get('city'),
            title=job.get('positionName'),
            salary=job.get('salary'),
            education=job.get('education'),
            nature=job.get('jobNature'),
            work_year=job.get('workYear'),
            advantage=job.get('positionAdvantage', ''),
            # job detail
            department=job_detail.get('department'),
            keywords=job_detail.get('keywords'),
            description=job_detail.get('description'),
        ))
    return jobs_dicts


def get_job_detail_from_lg(lg_job_id):
    """
    爬取职位详情页的数据

    返回的 dict 组成:
    department:
        type: str
        meaning: 招聘部门
        eg:  商业部
    keywords:
        type: List[str]
        meaning: 职位关键词
        eg: ['后端', 'Web', 'Python']
    description:
        type: List[str]
        meaning: 职位介绍
        eg: ['职位要求:', 'blablabla', '.......']

    :param lg_job_id: 接口使用的职位 id
    :return: 职位详情页数据
    :rtype: tornado.util.ObjectDict
    """
    response = utils.http_tools.requests_get(
        url=constants.JOB_DETAIL_URL.format(lg_job_id=lg_job_id))
    job_detail_html = etree.HTML(response.text)

    department = job_detail_html.xpath('//div[@class="job-name"]/div[@class="company"]/text()')
    description = job_detail_html.xpath('//dd[@class="job_bt"]/div//text()')
    keywords = job_detail_html.xpath('//dd[@class="job_request"]//li[@class="labels"]/text()')

    if not department:
        logger.error('can not get department by lg_job_id = {}, html is \n {}'.format(
            lg_job_id, response.text))

    return ObjectDict(
        department=department[0] if department else '',
        description=description,
        keywords=keywords,
    )


def clean_lg_job_data(job_dict):
    """
    清洗爬取到的职位信息

    :param job_dict: tornado.util.ObjectDict
    """
    if 'keywords' in job_dict:
        job_dict.keywords = set(map(lambda keyword: keyword.strip().lower(), job_dict.keywords))
    if 'description' in job_dict:
        job_dict.description = ''.join(job_dict.description) if job_dict.description else ''
        job_dict.description = job_dict.description[:constants.JOB_DESCRIPTION_MAX_LEN]
    if 'advantage' in job_dict:
        job_dict.advantage = job_dict.advantage[:constants.JOB_ADVANTAGE_MAX_LEN]
