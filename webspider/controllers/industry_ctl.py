# coding=utf-8
from sqlalchemy.exc import IntegrityError

from webspider.models.industry import IndustryModel


def insert_industry_if_not_exist(name):
    if IndustryModel.is_exist(filter_by={'name': name}):
        return
    try:
        industry_id = IndustryModel.add(name=name)
        return industry_id
    except IntegrityError:
        pass


def get_industry_id_by_name(name):
    industry = IndustryModel.get_one(filter_by={'name': name})
    if not industry:
        raise ValueError('Get None when industry name is {}'.format(name))
    return industry.id
