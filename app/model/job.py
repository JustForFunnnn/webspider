# -*- coding: utf-8 -*-
import time

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TEXT, TINYINT

from app.model.base import BaseModel


class JobModel(BaseModel):
    __tablename__ = 'job'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(64), doc=u'职位标题')
    work_year = Column(TINYINT, doc=u'工作年限要求')
    city_id = Column(INTEGER, doc=u'城市 id')
    company_id = Column(INTEGER, doc=u'公司 id')
    department = Column(VARCHAR(64), doc=u'招聘部门')
    salary = Column(VARCHAR(32), doc=u'薪水')
    education = Column(TINYINT, doc=u'教育背景要求')
    description = Column(TEXT, doc=u'额外描述')
    advantage = Column(VARCHAR(128), doc=u'职位优势')
    job_nature = Column(TINYINT, doc=u'工作性质')
    created_at = Column(INTEGER, default=time.time, doc=u'职位创建时间')
    updated_at = Column(INTEGER, default=time.time, onupdate=time.time, doc=u'职位创建时间')
