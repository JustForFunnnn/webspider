# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP

from webspider.models.base import BaseModel


class CompanyExtraModel(BaseModel):
    __tablename__ = 'company_extra'

    company_id = Column(INTEGER, nullable=False, primary_key=True)
    introduce = Column(VARCHAR, nullable=False, doc=u'公司简介')
    advantage = Column(VARCHAR, nullable=False, doc=u'公司优势')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, doc=u'创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'最后更新时间')
