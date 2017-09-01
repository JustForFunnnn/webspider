# -*- coding: utf-8 -*-
from functools import lru_cache

from common import constants
from app.model.job import JobModel
from app.controllers.city import CityController
from app.controllers.company import CompanyController
from app.controllers.jobs_count import JobsCountController
from app.utils.util import reverse_dict
from app.utils.util import get_salary_section
from app.utils.time_tools import timestamp2string


class JobController(object):
    @classmethod
    def add(cls, id, company_id, city_id, title, work_year='', department='', salary='', education='', description='',
            advantage='', job_nature='', created_at=0):
        JobModel.add(id=id, title=title, city_id=city_id, company_id=company_id, work_year=work_year,
                     department=department, salary=salary, education=education, description=description,
                     advantage=advantage, job_nature=job_nature, created_at=created_at)

    @classmethod
    def count(cls, id=None, keyword_id=None):
        return JobModel.count(id=id, keyword_id=keyword_id)

    @classmethod
    def list(cls, keyword_id=None, limit=None, offset=None):
        return JobModel.list(keyword_id=keyword_id, limit=limit, offset=offset)

    @classmethod
    @lru_cache(maxsize=constants.CACHE_SIZE)
    def get_jobs_statistics(cls, keyword_id):
        keyword_jobs_count = JobsCountController.list(keyword_id=keyword_id, sort_by='asc')
        for item in keyword_jobs_count:
            item.date_string = timestamp2string(timestamp=item.date, date_format='%m/%d')
        jobs = JobController.list(keyword_id=keyword_id)
        educations_request_counter = cls.educations_request_analyze(jobs=jobs)
        finance_stage_distribution = cls.finance_stage_distribution_analyze(jobs=jobs)
        city_jobs_counter = cls.city_jobs_count_analyze(jobs=jobs)
        salary_distribution = cls.salary_distribution_analyze(jobs=jobs)
        work_years_request_analyze = cls.work_years_request_analyze(jobs=jobs)
        return (keyword_jobs_count,
                educations_request_counter,
                finance_stage_distribution,
                city_jobs_counter,
                salary_distribution,
                work_years_request_analyze)

    @classmethod
    def work_years_request_analyze(cls, jobs):
        """分析职位的工作年限要求"""
        reversed_word_years_request_dict = reverse_dict(constants.WORK_YEARS_REQUEST_DICT)
        work_years_request_counter = {}
        for job in jobs:
            work_years_request = reversed_word_years_request_dict[job.work_year]
            if work_years_request in work_years_request_counter:
                work_years_request_counter[work_years_request] += 1
            else:
                work_years_request_counter[work_years_request] = 1
        return work_years_request_counter

    @classmethod
    def educations_request_analyze(cls, jobs):
        """分析职位的学历要求"""
        reversed_education_request_dict = reverse_dict(constants.EDUCATION_REQUEST_DICT)
        educations_request_counter = {}
        for job in jobs:
            education_request = reversed_education_request_dict[job.education]
            if education_request in educations_request_counter:
                educations_request_counter[education_request] += 1
            else:
                educations_request_counter[education_request] = 1
        return educations_request_counter

    @classmethod
    def finance_stage_distribution_analyze(cls, jobs):
        """分析招聘该职位的公司的融资分布情况"""
        company_ids = [job.company_id for job in jobs]
        companys = CompanyController.list(ids=company_ids)

        reversed_finance_stage_dict_dict = reverse_dict(constants.FINANCE_STAGE_DICT)
        # 特定排序的融资dict
        finance_stage_distribution = {
            '成熟型(不需要融资)': 0,
            '成长型(不需要融资)': 0,
            '初创型(不需要融资)': 0,
            '上市公司': 0,
            '成熟型(D轮及以上)': 0,
            '成熟型(C轮)': 0,
            '成长型(B轮)': 0,
            '成长型(A轮)': 0,
            '初创型(天使轮)': 0,
            '初创型(未融资)': 0,
        }
        for company in companys:
            finance_stage = reversed_finance_stage_dict_dict[company.finance_stage]
            if finance_stage in finance_stage_distribution:
                finance_stage_distribution[finance_stage] = finance_stage_distribution[finance_stage] + 1
        return finance_stage_distribution

    @classmethod
    def city_jobs_count_analyze(cls, jobs, limit=10):
        """统计各城市的招聘职位的数量"""
        city_jobs_counter = {}
        city_name_dict = CityController.get_city_name_dict()
        for job in jobs:
            city_name = city_name_dict[job.city_id]
            city_jobs_counter[city_name] = city_jobs_counter[city_name] + 1 if city_name in city_jobs_counter else 1
        city_jobs_counter = sorted(city_jobs_counter.items(), key=lambda x: x[1], reverse=True)[:limit]
        return city_jobs_counter

    @classmethod
    def salary_distribution_analyze(cls, jobs):
        """分析职位的薪水分布情况"""
        salary_distribution = {
            '10k 及以下': 0,
            '11k-20k': 0,
            '21k-35k': 0,
            '36k-60k': 0,
            '61k 以上': 0
        }
        for job in jobs:
            start_salary, end_salary = get_salary_section(job.salary)
            if start_salary <= 10:
                salary_distribution['10k 及以下'] += 1
            if start_salary <= 20 and end_salary >= 11:
                salary_distribution['11k-20k'] += 1
            if start_salary <= 35 and end_salary >= 21:
                salary_distribution['21k-35k'] += 1
            if start_salary <= 60 and end_salary >= 36:
                salary_distribution['36k-60k'] += 1
            if end_salary >= 61:
                salary_distribution['61k 以上'] += 1
        return salary_distribution
