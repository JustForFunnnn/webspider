# coding=utf-8
from webspider.models import CompanyModel


def get_company(company_id=None, lagou_company_id=None):
    if not any([company_id, lagou_company_id]):
        raise ValueError('必须指定过滤条件')
    filter_by = {}
    if company_id:
        filter_by['company_id'] = company_id

    if lagou_company_id:
        filter_by['lagou_company_id'] = lagou_company_id

    return CompanyModel.get_one(filter_by=filter_by)


def update_company(company_id, values):
    return CompanyModel.update(filter_by={'company_id': company_id}, values=values)


def add_company(values):
    return CompanyModel.add(**values)
