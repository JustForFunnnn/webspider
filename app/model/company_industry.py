# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER

from common.db import BaseModel


class CompanyIndustryModel(BaseModel):
    __tablename__ = 'company_industry'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    company_id = Column(INTEGER, doc=u'公司 id')
    industry_id = Column(INTEGER, doc=u'行业 id')
    city_id = Column(INTEGER, doc=u'冗余:所在城市 id')

    @classmethod
    def list(cls, company_id=None):
        query = cls.session.query(cls)
        if company_id:
            query = query.filter(cls.company_id == company_id)
        return query.all()

    @classmethod
    def add(cls, company_id, industry_id, city_id):
        company_industry = cls(company_id=int(company_id), industry_id=int(industry_id), city_id=int(city_id))
        cls.session.merge(company_industry)
        cls.session.flush()
