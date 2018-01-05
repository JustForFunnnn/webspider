# coding=utf-8
import logging

from webspider import utils
from webspider.models import (CityModel, CompanyModel, CompanyExtraModel, CompanyIndustryModel)
from webspider.scripts.crawler.lagou_cites import crawl_lagou_cites
from webspider.scripts.crawler import lagou_companies as lagou_companies_scripts
from webspider.scripts.crawler.lagou_companies import crawl_lagou_companies

from webspider.controllers import industry_ctl

logger = logging.getLogger(__name__)


def crawl_lagou_data_suites():
    # city_dicts = crawl_lagou_cites()
    #
    # for city_dict in city_dicts:
    #     if CityModel.is_exist(pk=city_dict.id):
    #         CityModel.update_by_pk(pk=city_dict.id, values=city_dict)
    #     else:
    #         CityModel.add(**city_dict)

    # # 北京:2 上海:3 深圳:215 广州:213 杭州:6 成都:252
    # city_ids = [2, 3, 6, 79, 184, 213, 215, 298, 252]
    # finance_stage_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    # industry_ids = [0, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 38, 41, 43, 45, 47, 48, 49, 10594]
    companies_pagination = lagou_companies_scripts.crawl_lagou_companies_pagination(city_id=2, finance_stage_id=1,
                                                                                    industry_id=24)
    for page_no in companies_pagination.iter_pages:
        company_dicts = lagou_companies_scripts.crawl_lagou_companies(city_id=2, finance_stage_id=1, industry_id=24,
                                                                      page_no=page_no)
        print('第{}页, {}个公司'.format(page_no, len(company_dicts)))
        if not company_dicts:
            print('爬虫在第{}页时结束'.format(page_no))
            break
        for company_dict in company_dicts:
            if CompanyModel.is_exist(filter_by={'lagou_company_id': company_dict.lagou_company_id}):
                print('跳过 {}'.format(company_dict.lagou_company_id))
                continue
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






                # for city_id in city_ids:
                #     for finance_stage_id in finance_stage_ids:
                #         for industry_id in industry_ids:
                #             companies_pagination = crawl_lagou_companies_pagination(city_id=city_id,
                #                                                                     finance_stage_id=finance_stage_id,
                #                                                                     industry_id=industry_id)
