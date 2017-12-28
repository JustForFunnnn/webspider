# -*- coding: utf-8 -*-
import time
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TEXT, TINYINT, TIMESTAMP

from webspider.model.base import BaseModel


class JobModel(BaseModel):
    __tablename__ = 'job'

    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    city_id = Column(INTEGER, nullable=False, doc=u'城市 id')
    company_id = Column(INTEGER, nullable=False, doc=u'公司 id')
    title = Column(VARCHAR(64), nullable=False, default='', doc=u'职位标题')
    work_year = Column(TINYINT, nullable=False, doc=u'工作年限要求')
    department = Column(VARCHAR(64), nullable=False, doc=u'招聘部门')
    salary = Column(VARCHAR(32), nullable=False, doc=u'薪水')
    education = Column(TINYINT, nullable=False, doc=u'教育背景要求')
    description = Column(VARCHAR(10000), nullable=False, doc=u'额外描述')
    advantage = Column(VARCHAR(128), nullable=False, doc=u'职位优势')
    nature = Column(TINYINT, nullable=False, doc=u'工作性质')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, doc=u'职位创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'职位创建时间')
