# coding=utf-8
from webspider.model.company import CompanyModel


class CompanyController(object):
    @classmethod
    def add(cls, id, shortname, fullname, city_id, finance_stage=0, process_rate=0, features='', introduce='',
            address='', advantage='', size=''):
        return CompanyModel.add(id=id, shortname=shortname, fullname=fullname, finance_stage=finance_stage,
                                city_id=city_id, process_rate=process_rate, features=features, introduce=introduce,
                                address=address, advantage=advantage, size=size)

    @classmethod
    def list(cls, ids, city_id=None):
        return CompanyModel.list(ids=ids, city_id=city_id)

    @classmethod
    def update(cls, id, update_attr):
        affect_rows = CompanyModel.update(id=id, update_attr=update_attr)
        return affect_rows

    @classmethod
    def get_company_last_update_time(cls):
        company = CompanyModel.list(limit=1)
        return company[0].updated_at if len(company) != 0 else None

    @classmethod
    def count(cls, id=None):
        return CompanyModel.count(id=id)
