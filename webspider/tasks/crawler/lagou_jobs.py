# coding=utf-8
import logging

from lxml import etree
from tornado.util import ObjectDict

from webspider import utils
from webspider import constants
from webspider.controllers import city_ctl
from webspider.models.job import JobModel

logger = logging.getLogger(__name__)


def crawl_lagou_jobs_pagination(lagou_company_id, job_type, page_no=1, school_job=False):
    """
    获取拉勾职位 分页数据
    :param lagou_company_id: 拉勾公司 id
    :return: utils.pagination.Pagination instance
    """
    params = {
        'companyId': lagou_company_id,
        'positionFirstType': job_type,
        'schoolJob': school_job,
        'pageNo': page_no,
        'pageSize': 10,
    }
    response_json = utils.http_tools.requests_get(url=constants.COMPANY_JOBS_URL, params=params).json()
    pagination = utils.pagination.Pagination(per_page=int(response_json['content']['data']['page']['pageSize']),
                                             total=int(response_json['content']['data']['page']['totalCount']))

    return pagination


def crawl_lagou_jobs(lagou_company_id, job_type, page_no=1, school_job=False, skip_exist=True):
    params = {
        'companyId': lagou_company_id,
        'positionFirstType': job_type,
        'schoolJob': school_job,
        'pageNo': page_no,
        'pageSize': 10,
    }
    response_json = utils.http_tools.requests_get(url=constants.COMPANY_JOBS_URL, params=params).json()
    jobs = response_json['content']['data']['page']['result']

    jobs_dicts = []
    for job in jobs:
        lagou_job_id = job['positionId']
        if skip_exist and JobModel.is_exist(filter_by={'lagou_job_id': lagou_job_id}):
            print('跳过 job, lagou job id is {}'.format(lagou_job_id))
            continue

        job_detail = crawl_lagou_job_detail(lagou_job_id=lagou_job_id)
        jobs_dicts.append(ObjectDict(
            lagou_job_id=lagou_job_id,
            city=job.get('city'),
            title=job.get('positionName'),
            salary=job.get('salary'),
            education=job.get('education'),
            nature=job.get('jobNature'),
            work_year=job.get('workYear'),
            advantage=job.get('positionAdvantage'),
            # job detail
            department=job_detail.get('department'),
            keywords=job_detail.get('keywords'),
            description=job_detail.get('description'),
        ))
    return jobs_dicts


def crawl_lagou_job_detail(lagou_job_id):
    response = utils.http_tools.requests_get(url=constants.JOB_DETAIL_URL.format(lagou_job_id=lagou_job_id))
    job_detail_html = etree.HTML(response.text)

    department = job_detail_html.xpath('//div[@class="job-name"]/div[@class="company"]/text()')
    description = job_detail_html.xpath('//dd[@class="job_bt"]/div//text()')
    keywords = job_detail_html.xpath('//dd[@class="job_request"]//li[@class="labels"]/text()')

    if not department:
        logger.error('can not get department by lagou_job_id = {}'.format(lagou_job_id))

    return ObjectDict(
        department=department[0] if department else '',
        description=description,
        keywords=keywords,
    )


def clean_lagou_job_data(job_dict):
    if 'keywords' in job_dict:
        job_dict.keywords = set(map(lambda keyword: keyword.strip().lower(), job_dict.keywords))
    if 'description' in job_dict:
        job_dict.description = ''.join(job_dict.description) if job_dict.description else ''
        job_dict.description = job_dict.description[:constants.JOB_DESCRIPTION_MAX_LEN]
    if 'advantage' in job_dict:
        job_dict.advantage = job_dict.advantage[:constants.JOB_ADVANTAGE_MAX_LEN]


def convert_lagou_job_data(job_dict):
    if job_dict.nature not in constants.JOB_NATURE_DICT:
        logger.error(
            '{} not in constants.JOB_NATURE_DICT, lagou job id is {}'.format(job_dict.nature,
                                                                             job_dict.lagou_job_id))
    job_dict.nature = constants.JOB_NATURE_DICT.get(job_dict.nature, constants.JOB_NATURE_DICT['unknown'])

    if job_dict.work_year not in constants.WORK_YEARS_REQUEST_DICT:
        logger.error(
            '{} not in constants.WORK_YEARS_REQUEST_DICT, lagou job id is {}'.format(job_dict.work_year,
                                                                                     job_dict.lagou_job_id))
    job_dict.work_year = constants.WORK_YEARS_REQUEST_DICT.get(job_dict.work_year,
                                                               constants.WORK_YEARS_REQUEST_DICT['unknown'])

    if job_dict.education not in constants.EDUCATION_REQUEST_DICT:
        logger.error(
            '{} not in constants.EDUCATION_REQUEST_DICT, lagou job id is {}'.format(job_dict.education,
                                                                                    job_dict.lagou_job_id))
    job_dict.education = constants.EDUCATION_REQUEST_DICT.get(job_dict.education,
                                                              constants.EDUCATION_REQUEST_DICT['unknown'])

    job_dict.city_id = city_ctl.get_city_id_by_name(job_dict.city)
