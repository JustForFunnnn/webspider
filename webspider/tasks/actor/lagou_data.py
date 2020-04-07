# coding=utf-8
import logging

from webspider import utils
from webspider import crawlers
from webspider import constants
from webspider.utils.cache import redis_instance
from webspider.tasks.celery_app import celery_app
from webspider.controllers import industry_ctl, keyword_ctl, city_ctl
from webspider.models import (CityModel, CompanyModel,
                              CompanyIndustryModel, JobModel, JobKeywordModel)

logger = logging.getLogger(__name__)


@celery_app.task()
def crawl_lg_data_task():
    """爬取数据任务"""

    # 清除抓取记录
    keys = redis_instance.keys('crawled_company_jobs*')
    if keys:
        redis_instance.delete(*keys)

    crawl_lg_city_data_task.delay()
    # 目前只抓取这几个城市 全国:0, 北京:2 上海:3 杭州:6 深圳:215 广州:213 成都:252
    lg_city_ids = [2, 3, 6, 215, 213, 252]
    lg_finance_stage_ids = [1, 2, 3, 4, 5, 6, 7, 8]
    lg_industry_ids = [24, 25, 33, 27, 29, 45, 31, 28,
                       47, 34, 35, 43, 32, 41, 26, 48, 38, 49, 10594]
    # 爬取公司数据
    for industry_id in lg_industry_ids:
        for city_id in lg_city_ids:
            for finance_stage_id in lg_finance_stage_ids:
                crawl_lg_company_data_task.delay(city_id=city_id, finance_stage_id=finance_stage_id,
                                                 industry_id=industry_id)


@celery_app.task()
def crawl_lg_city_data_task():
    """爬取城市数据任务"""
    city_dicts = crawlers.get_cites_from_lg()
    for city_dict in city_dicts:
        if CityModel.is_exist(filter_by={'id': city_dict.id}):
            CityModel.update_by_pk(pk=city_dict.id, values=city_dict)
        else:
            CityModel.add(**city_dict)


@celery_app.task()
def crawl_lg_company_data_task(city_id, finance_stage_id, industry_id):
    """爬取公司数据任务"""
    companies_pagination = crawlers.get_companies_pagination_from_lg(city_id=city_id,
                                                                     finance_stage_id=finance_stage_id,
                                                                     industry_id=industry_id)
    for page_no in companies_pagination.iter_pages:
        company_dicts = crawlers.get_companies_from_lg(city_id=city_id,
                                                       finance_stage_id=finance_stage_id,
                                                       industry_id=industry_id,
                                                       page_no=page_no)
        if not company_dicts:
            break
        for company_dict in company_dicts:
            crawlers.clean_lg_company_data(company_dict)
            utils.convert.convert_dict_field_to_constants(company_dict)

            industries = company_dict.pop('industries')
            city_name = company_dict.pop('city_name')

            city_ctl.insert_city_if_not_exist(city_name)
            company_dict['city_id'] = city_ctl.get_city_id_by_name(city_name)

            company = CompanyModel.get_one(
                filter_by={'lg_company_id': company_dict.lg_company_id})
            if company:
                CompanyModel.update_by_pk(pk=company.id, values=company_dict)
            else:
                company_id = CompanyModel.add(**company_dict)

                for industry in industries:
                    industry_ctl.insert_industry_if_not_exist(name=industry)
                    industry_id = industry_ctl.get_industry_id_by_name(name=industry)
                    CompanyIndustryModel.add(industry_id=industry_id, company_id=company_id)

            crawl_lg_job_data_task.delay(company_dict.lg_company_id)


@celery_app.task()
def crawl_lg_job_data_task(lg_company_id):
    """爬取职位数据任务"""
    # 过滤本轮已经爬取过职位的公司
    if not redis_instance.setnx(constants.CRAWLED_COMPANY_JOBS_REDIS_KEY.format(lg_company_id=lg_company_id), 1):
        return
    jobs_pagination = crawlers.get_jobs_pagination_from_lg(lg_company_id=lg_company_id,
                                                           job_type=constants.LGJobType.technology)
    for page_no in jobs_pagination.iter_pages:
        job_dicts = crawlers.get_jobs_from_lg(lg_company_id=lg_company_id,
                                              job_type=constants.LGJobType.technology,
                                              page_no=page_no)
        if not job_dicts:
            break
        for job_dict in job_dicts:
            crawlers.clean_lg_job_data(job_dict)
            utils.convert.convert_dict_field_to_constants(job_dict)

            keywords = job_dict.pop('keywords')
            city_name = job_dict.pop('city_name')

            city_ctl.insert_city_if_not_exist(city_name)
            job_dict['city_id'] = city_ctl.get_city_id_by_name(city_name)
            company = CompanyModel.get_one(filter_by={'lg_company_id': lg_company_id})
            job_dict['company_id'] = company.id

            job = JobModel.get_one(filter_by={'lg_job_id': job_dict.lg_job_id})
            if job:
                JobModel.update_by_pk(pk=job.id, values=job_dict)
            else:
                job_id = JobModel.add(**job_dict)

                for keyword in keywords:
                    keyword_ctl.insert_keyword_if_not_exist(name=keyword)
                    keyword_id = keyword_ctl.get_keyword_id_by_name(name=keyword)
                    JobKeywordModel.add(keyword_id=keyword_id, job_id=job_id)
