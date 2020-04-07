# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP

from webspider.models.base import BaseModel


class CompanyIndustryModel(BaseModel):
    __tablename__ = 'company_industry'

    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    company_id = Column(INTEGER, nullable=False, doc=u'公司 id')
    industry_id = Column(INTEGER, nullable=False, doc=u'行业 id')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, doc=u'创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'最后更新时间')
