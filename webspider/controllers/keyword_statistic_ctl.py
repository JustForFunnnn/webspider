# -*- coding: utf-8 -*-
from collections import Counter

from webspider import utils
from webspider import constants
from webspider.models import CompanyModel
from webspider.controllers import city_ctl, job_ctl


def get_salary_statistic(jobs):
    """
    获取薪水统计情况

    :param jobs: webspider.models.JobModel instances list
    :return: collections.Counter
    """
    salary_statistic = Counter()
    for job in jobs:
        start_salary, end_salary = job_ctl.get_salary_section(job.salary)
        if start_salary <= 10:
            salary_statistic['10k及以下'] += 1
        if start_salary <= 20 and end_salary >= 11:
            salary_statistic['11k-20k'] += 1
        if start_salary <= 35 and end_salary >= 21:
            salary_statistic['21k-35k'] += 1
        if start_salary <= 60 and end_salary >= 36:
            salary_statistic['36k-60k'] += 1
        if end_salary >= 61:
            salary_statistic['61k以上'] += 1
    return salary_statistic


def get_finance_stage_statistic(jobs):
    """
    获取 jobs 的公司的统治情况统计

    :param jobs: webspider.models.JobModel instances list
    :return: collections.Counter
    """
    company_ids = [job.company_id for job in jobs]
    companies = CompanyModel.list(filter=CompanyModel.id.in_(company_ids))

    finance_stage_statistic = utils.common.get_field_statistics(values=[company.finance_stage for company in companies],
                                                                constants_dict=constants.FINANCE_STAGE_DICT)
    return finance_stage_statistic


def get_educations_statistic(jobs):
    """
    获取教育背景要求统计

    :param jobs: webspider.models.JobModel instances list
    :return: collections.Counter
    """
    return utils.common.get_field_statistics(values=[job.education for job in jobs],
                                             constants_dict=constants.EDUCATION_REQUEST_DICT)


def get_work_years_statistic(jobs):
    """
    获取工作年限要求统计

    :param jobs: webspider.models.JobModel instances list
    :return: collections.Counter
    """
    return utils.common.get_field_statistics(values=[job.work_year for job in jobs],
                                             constants_dict=constants.WORK_YEARS_REQUEST_DICT)


def get_city_jobs_count_statistic(jobs, limit=10):
    """
    获取各城市职位统计
    :param jobs: webspider.models.JobModel instances list
    :param limit: 指定获取职位数量前几位的城市
    :return: collections.Counter
    """
    city_name_dict = city_ctl.get_city_name_dict()
    city_job_count = utils.common.get_field_statistics(values=[job.city_id for job in jobs],
                                                       constants_dict=city_name_dict)
    city_job_count = sorted(city_job_count.items(), key=lambda x: x[1], reverse=True)
    if limit:
        city_job_count = city_job_count[:limit]
    return Counter({item[0]: item[1] for item in city_job_count})
