# coding=utf-8
from webspider.model.industry import IndustryModel


class IndustryController(object):
    @classmethod
    def get(cls, name):
        industry = IndustryModel.get(name=name)
        return industry

    @classmethod
    def get_industry_id_by_name(cls, name):
        IndustryModel.insert_if_not_exist(name=name)
        industry = IndustryModel.get(name=name)
        return industry.id
