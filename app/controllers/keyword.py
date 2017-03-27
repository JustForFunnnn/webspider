# coding=utf-8
from functools import lru_cache

from app.controllers.job import JobController
from app.controllers.city import CityController
from app.controllers.company import CompanyController
from app.controllers.job_keyword import JobKeywordController
from app.model.keyword import KeywordModel
from app.utils.util import reverse_dict, get_salary_section, update_salary_dict
from common.constants import EDUCATION_DICT, WORK_YEAR_DICT, COMPANY_SIZE_DICT, FINANCE_STAGE_DICT


class KeywordController(object):
    @classmethod
    def get(cls, name):
        return KeywordModel.get(name=name)

    @classmethod
    def get_keyword_id_by_name(cls, name):
        KeywordModel.insert_if_not_exist(name=name)
        keyword = KeywordModel.get(name=name)
        return keyword.id

    @classmethod
    @lru_cache(maxsize=128)
    def keyword_analyze(cls, keyword_id):
        jobs = JobController.list(keyword_id=keyword_id)
        company_ids = set()
        education_name_dict = reverse_dict(EDUCATION_DICT)
        work_year_name_dict = reverse_dict(WORK_YEAR_DICT)
        company_size_name_dict = reverse_dict(COMPANY_SIZE_DICT)
        finance_stage_name_dict = reverse_dict(FINANCE_STAGE_DICT)
        city_name_dict = CityController.get_city_name_dict()

        work_year_dict, education_dict, city_dict, salary_dict = {}, {}, {}, {}
        for job in jobs:
            work_year = work_year_name_dict[job.work_year]
            education = education_name_dict[job.education]
            city = city_name_dict[job.city_id]
            work_year_dict[work_year] = work_year_dict[work_year] + 1 if work_year in work_year_dict else 1
            education_dict[education] = education_dict[education] + 1 if education in education_dict else 1
            city_dict[city] = city_dict[city] + 1 if city in city_dict else 1
            company_ids.add(job.company_id)
            start_salary, end_salary = get_salary_section(job.salary)
            salary_dict = update_salary_dict(salary_dict, start=start_salary, end=end_salary)

        companys = CompanyController.list(ids=company_ids)
        company_size_dict = {}
        finance_stage_dict = {
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
            company_size = company_size_name_dict[company.size]
            finance_stage = finance_stage_name_dict[company.finance_stage]
            company_size_dict[company_size] = company_size_dict[
                                                  company_size] + 1 if company_size in company_size_dict else 1
            if finance_stage in finance_stage_dict:
                finance_stage_dict[finance_stage] = finance_stage_dict[finance_stage] + 1
        city_dict = sorted(city_dict.items(), key=lambda x: x[1], reverse=True)[:10]
        return work_year_dict, education_dict, city_dict, salary_dict, finance_stage_dict

    @classmethod
    def get_most_frequently_keywords(cls):
        return JobKeywordController.get_most_frequently_keywords()
