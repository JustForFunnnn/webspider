# coding=utf-8
import logging

from webspider import utils
from webspider import crawlers
from webspider import constants
from webspider.tasks.celery_app import celery_app
from webspider.controllers import industry_ctl, keyword_ctl, city_ctl
from webspider.models import (CityModel, CompanyModel, CompanyExtraModel, CompanyIndustryModel, JobModel, JobExtraModel,
                              JobKeywordModel)

logger = logging.getLogger(__name__)


@celery_app.task()
def crawl_lagou_data_task(use_celery=True):
    # 目前只抓取这几个城市 全国:0, 北京:2 上海:3 杭州:6 深圳:215 广州:213 成都:252
    lagou_city_ids = [2, 3, 6, 215, 213, 252]
    lagou_finance_stage_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    lagou_industry_ids = [24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 38, 41, 43, 45, 47, 48, 49, 10594]
    # 爬取公司数据
    for city_id in lagou_city_ids:
        for industry_id in lagou_industry_ids:
            for finance_stage_id in lagou_finance_stage_ids:
                if use_celery:
                    crawl_lagou_company_data_task.delay(city_id=city_id, finance_stage_id=finance_stage_id,
                                                        industry_id=industry_id, use_celery=use_celery)
                else:
                    crawl_lagou_company_data_task(city_id=city_id, finance_stage_id=finance_stage_id,
                                                  industry_id=industry_id, use_celery=use_celery)


@celery_app.task()
def crawl_lagou_city_data_task():
    city_dicts = crawlers.get_cites_from_lagou()
    for city_dict in city_dicts:
        if CityModel.is_exist(filter_by={'id': city_dict.id}):
            CityModel.update_by_pk(pk=city_dict.id, values=city_dict)
        else:
            CityModel.add(**city_dict)


@celery_app.task()
def crawl_lagou_company_data_task(city_id, finance_stage_id, industry_id, use_celery=True):
    companies_pagination = crawlers.get_companies_pagination_from_lagou(city_id=city_id,
                                                                        finance_stage_id=finance_stage_id,
                                                                        industry_id=industry_id)
    for page_no in companies_pagination.iter_pages:
        company_dicts = crawlers.get_companies_from_lagou(city_id=city_id,
                                                          finance_stage_id=finance_stage_id,
                                                          industry_id=industry_id,
                                                          page_no=page_no)
        if not company_dicts:
            break
        for company_dict in company_dicts:
            crawlers.clean_lagou_company_data(company_dict)
            utils.convert.convert_dict_field_to_constants(company_dict)

            industries = company_dict.pop('industries')
            advantage = company_dict.pop('advantage')
            introduce = company_dict.pop('introduce')
            city_name = company_dict.pop('city_name')

            city_ctl.insert_city_if_not_exist(city_name)
            company_dict['city_id'] = city_ctl.get_city_id_by_name(city_name)

            company = CompanyModel.get_one(filter_by={'lagou_company_id': company_dict.lagou_company_id})
            if company:
                CompanyModel.update_by_pk(pk=company.id, values=company_dict)
                CompanyExtraModel.update_by_pk(pk=company.id, values=dict(introduce=introduce, advantage=advantage))
            else:
                company_id = CompanyModel.add(**company_dict)
                CompanyExtraModel.add(introduce=introduce, company_id=company_id, advantage=advantage)

                for industry in industries:
                    industry_ctl.insert_industry_if_not_exist(name=industry)
                    industry_id = industry_ctl.get_industry_id_by_name(name=industry)
                    CompanyIndustryModel.add(industry_id=industry_id, company_id=company_id)

            if use_celery:
                crawl_lagou_job_data_task.delay(company_dict.lagou_company_id)
            else:
                crawl_lagou_job_data_task(company_dict.lagou_company_id)


@celery_app.task()
def crawl_lagou_job_data_task(lagou_company_id):
    jobs_pagination = crawlers.get_jobs_pagination_from_lagou(lagou_company_id=lagou_company_id,
                                                              job_type=constants.LagouJobType.technology)
    for page_no in jobs_pagination.iter_pages:
        job_dicts = crawlers.get_jobs_from_lagou(lagou_company_id=lagou_company_id,
                                                 job_type=constants.LagouJobType.technology,
                                                 page_no=page_no)
        if not job_dicts:
            break
        for job_dict in job_dicts:
            crawlers.clean_lagou_job_data(job_dict)
            utils.convert.convert_dict_field_to_constants(job_dict)
            company = CompanyModel.get_one(filter_by={'lagou_company_id': lagou_company_id})

            keywords = job_dict.pop('keywords')
            advantage = job_dict.pop('advantage')
            description = job_dict.pop('description')
            city_name = job_dict.pop('city_name')

            city_ctl.insert_city_if_not_exist(city_name)
            job_dict['city_id'] = city_ctl.get_city_id_by_name(city_name)
            job_dict['company_id'] = company.id

            job = JobModel.get_one(filter_by={'lagou_job_id': job_dict.lagou_job_id})
            if job:
                JobModel.update_by_pk(pk=job.id, values=job_dict)
                JobKeywordModel.update_by_pk(pk=job.id, values=dict(advantage=advantage, description=description))
            else:
                job_id = JobModel.add(**job_dict)
                JobExtraModel.add(advantage=advantage, description=description, job_id=job_id)

                for keyword in keywords:
                    keyword_ctl.insert_keyword_if_not_exist(name=keyword)
                    keyword_id = keyword_ctl.get_keyword_id_by_name(name=keyword)
                    JobKeywordModel.add(keyword_id=keyword_id, job_id=job_id)
