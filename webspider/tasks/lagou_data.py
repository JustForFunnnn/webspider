# coding=utf-8
import logging

from webspider import constants
from webspider.models import (CityModel, CompanyModel, CompanyExtraModel, CompanyIndustryModel, JobModel, JobExtraModel,
                              JobKeywordModel)
from webspider.tasks.crawler import lagou_cites as lagou_cites_scripts
from webspider.tasks.crawler import lagou_companies as lagou_companies_scripts
from webspider.tasks.crawler import lagou_jobs as lagou_jobs_scripts
from webspider.controllers import industry_ctl, keyword_ctl

logger = logging.getLogger(__name__)


def crawl_lagou_data_task():
    # 目前只抓取这几个城市 全国:0, 北京:2 上海:3 深圳:215 广州:213 杭州:6 成都:252
    city_ids = [0, 2, 3, 6, 79, 184, 213, 215, 298, 252]
    finance_stage_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    industry_ids = [0, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 38, 41, 43, 45, 47, 48, 49, 10594]
    # 爬取城市数据
    crawl_lagou_city_data_suites()
    # 爬取公司数据
    for city_id in city_ids:
        for finance_stage_id in finance_stage_ids:
            for industry_id in industry_ids:
                crawl_lagou_company_data_suites(city_id=city_id, finance_stage_id=finance_stage_id,
                                                industry_id=industry_id)


def crawl_lagou_city_data_suites():
    city_dicts = lagou_cites_scripts.crawl_lagou_cites()

    for city_dict in city_dicts:
        if CityModel.is_exist(pk=city_dict.id):
            CityModel.update_by_pk(pk=city_dict.id, values=city_dict)
        else:
            CityModel.add(**city_dict)


def crawl_lagou_company_data_suites(city_id, finance_stage_id, industry_id):
    companies_pagination = lagou_companies_scripts.crawl_lagou_companies_pagination(city_id=city_id,
                                                                                    finance_stage_id=finance_stage_id,
                                                                                    industry_id=industry_id)
    for page_no in companies_pagination.iter_pages:
        company_dicts = lagou_companies_scripts.crawl_lagou_companies(city_id=city_id,
                                                                      finance_stage_id=finance_stage_id,
                                                                      industry_id=industry_id,
                                                                      page_no=page_no)
        if not company_dicts:
            print('city_id {}, finance_stage_id {}, industry_id {}, 爬取到第 {} 页时跳出'.format(city_id, finance_stage_id,
                                                                                         industry_id, page_no))
            break
        for company_dict in company_dicts:
            lagou_companies_scripts.clean_lagou_company_data(company_dict)
            lagou_companies_scripts.convert_lagou_company_data(company_dict)

            industries = company_dict.pop('industries')
            advantage = company_dict.pop('advantage')
            introduce = company_dict.pop('introduce')
            company_dict.pop('city')

            company_id = CompanyModel.add(**company_dict)
            CompanyExtraModel.add(introduce=introduce, company_id=company_id, advantage=advantage)

            for industry in industries:
                industry_ctl.insert_industry_if_not_exist(name=industry)
                industry_id = industry_ctl.get_industry_id_by_name(name=industry)
                CompanyIndustryModel.add(industry_id=industry_id, company_id=company_id)
            crawl_lagou_job_data_suites(company_dict.lagou_company_id)


def crawl_lagou_job_data_suites(lagou_company_id):
    jobs_pagination = lagou_jobs_scripts.crawl_lagou_jobs_pagination(lagou_company_id=lagou_company_id,
                                                                     job_type=constants.LagouJobType.technology)
    print('爬取 lagou_company_id {}, 总共 {} 页， 数据总共 {} 条'.format(lagou_company_id, jobs_pagination.pages,
                                                              jobs_pagination.total))
    for page_no in jobs_pagination.iter_pages:
        job_dicts = lagou_jobs_scripts.crawl_lagou_jobs(lagou_company_id=lagou_company_id,
                                                        job_type=constants.LagouJobType.technology,
                                                        page_no=page_no)
        if not job_dicts:
            print('lagou_company_id is {}, 爬取到第 {} 页时跳出'.format(lagou_company_id, page_no))
            break
        for job_dict in job_dicts:
            lagou_jobs_scripts.clean_lagou_job_data(job_dict)
            lagou_jobs_scripts.convert_lagou_job_data(job_dict)

            company = CompanyModel.get_one(filter_by={'lagou_company_id': lagou_company_id})
            job_dict['company_id'] = company.id
            keywords = job_dict.pop('keywords')
            advantage = job_dict.pop('advantage')
            description = job_dict.pop('description')
            job_dict.pop('city')

            job_id = JobModel.add(**job_dict)
            JobExtraModel.add(advantage=advantage, description=description, job_id=job_id)

            for keyword in keywords:
                keyword_ctl.insert_keyword_if_not_exist(name=keyword)
                keyword_id = keyword_ctl.get_keyword_id_by_name(name=keyword)
                JobKeywordModel.add(keyword_id=keyword_id, job_id=job_id)
