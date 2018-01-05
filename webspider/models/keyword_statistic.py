# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP

from webspider.models.base import BaseModel


class KeywordStatisticModel(BaseModel):
    __tablename__ = 'keyword_statistic'

    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    keyword_id = Column(INTEGER, nullable=False, doc=u'关键词 id')
    educations = Column(VARCHAR(2048), nullable=False, doc=u'教育背景要求统计')
    jobs_count = Column(VARCHAR(2048), nullable=False, doc=u'职位数量统计')
    salary = Column(VARCHAR(2048), nullable=False, doc=u'薪水分布统计')
    financing_stage = Column(VARCHAR(2048), nullable=False, doc=u'招聘公司的融资统计')
    work_years = Column(VARCHAR(2048), nullable=False, doc=u'职位薪水统计')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, doc=u'创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'创建时间')
