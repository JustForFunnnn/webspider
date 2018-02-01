# -*- coding: utf-8 -*-
import re
from collections import Counter

from webspider import utils
from webspider import constants
from webspider.models import CompanyModel, KeywordStatisticModel
from webspider.controllers import city_ctl

ONE_TIME_MAX_RESULT = 10000


def get_keyword_statistic(keyword_id):
    return KeywordStatisticModel.get_one(filter_by={'keyword_id': keyword_id})


def update_salary_dict(salary_dict, start, end):
    if len(salary_dict) == 0:
        salary_dict = {i: 0 for i in range(0, 111)}
    for index in range(start, end + 1):
        salary_dict[index] += 1
    return salary_dict


def get_salary_section(string):
    """
    e.g:
    15k-25k  ->  (15, 25)
    15k以上  ->  (15, 20)
    15k以下  ->  (10, 15)
    :param string: 15k-25k
    :return: 15,25
    """
    pattern = r'K|k|以上|以下'
    replace_char = ''

    if string.find('-') != -1:
        string = re.sub(pattern=pattern, repl=replace_char, string=string)
        start, end = string.split('-')
    elif string.endswith('以下'):
        string = re.sub(pattern=pattern, repl=replace_char, string=string)
        start, end = int(string) - 5 if int(string) - 5 >= 0 else 1, string
    elif string.endswith('以上'):
        string = re.sub(pattern=pattern, repl=replace_char, string=string)
        start, end = string, int(string) + 5
    else:
        raise ValueError('error salary' + string)

    return int(start), int(end)


def get_salary_statistic(jobs):
    """职位的薪水分布情况"""
    salary_statistic = Counter()
    for job in jobs:
        start_salary, end_salary = get_salary_section(job.salary)
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
    company_ids = [job.company_id for job in jobs]
    companies = CompanyModel.list(filter=CompanyModel.id.in_(company_ids))

    finance_stage_statistic = utils.common.get_field_statistics(values=[company.finance_stage for company in companies],
                                                                constants_dict=constants.FINANCE_STAGE_DICT)
    return finance_stage_statistic


def get_educations_statistic(jobs):
    return utils.common.get_field_statistics(values=[job.education for job in jobs],
                                             constants_dict=constants.EDUCATION_REQUEST_DICT)


def get_work_years_statistic(jobs):
    return utils.common.get_field_statistics(values=[job.work_year for job in jobs],
                                             constants_dict=constants.WORK_YEARS_REQUEST_DICT)


def get_sorted_city_jobs_count_statistic(jobs, limit=10):
    city_name_dict = city_ctl.get_city_name_dict()
    city_job_count = utils.common.get_field_statistics(values=[job.city_id for job in jobs],
                                                       constants_dict=city_name_dict)
    sorted_city_job_count = sorted(city_job_count.items(), key=lambda x: x[1], reverse=True)
    if limit:
        sorted_city_job_count = sorted_city_job_count[:limit]
    return Counter({item[0]: item[1] for item in sorted_city_job_count})
