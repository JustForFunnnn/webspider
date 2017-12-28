# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER

from common.db import BaseModel


class CompanyIndustryModel(BaseModel):
    __tablename__ = 'company_industry'

    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    company_id = Column(INTEGER, nullable=False, doc=u'公司 id')
    industry_id = Column(INTEGER, nullable=False, doc=u'行业 id')
