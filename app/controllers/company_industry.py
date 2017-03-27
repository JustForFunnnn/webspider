# -*- coding: utf-8 -*-
from app.model.company_industry import CompanyIndustryModel


class CompanyIndustryController(object):
    @classmethod
    def add(cls, company_id, industry_id, city_id):
        return CompanyIndustryModel.add(company_id=company_id, industry_id=industry_id, city_id=city_id)
