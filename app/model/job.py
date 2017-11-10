# -*- coding: utf-8 -*-
import time

from sqlalchemy import Column, func, and_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TEXT, TINYINT

from common.db import BaseModel
from app.model.job_keyword import JobKeywordModel


class JobModel(BaseModel):
    __tablename__ = 'job'

    id = Column(INTEGER, primary_key=True)
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
    created_at = Column(INTEGER, doc=u'职位创建时间')
    updated_at = Column(INTEGER, default=time.time, onupdate=time.time, doc=u'职位创建时间')

    @classmethod
    def add(cls, id, company_id, city_id, title, work_year=0, department='', salary='', education=0, description='',
            advantage='', job_nature=0, created_at=0):
        job = cls(id=id, title=title, city_id=city_id, company_id=company_id, work_year=int(work_year),
                  department=department, salary=salary, education=int(education), description=description,
                  advantage=advantage, job_nature=int(job_nature), created_at=created_at)
        try:
            cls.session.merge(job)
            cls.session.flush()
        except InvalidRequestError as e:
            cls.session.rollback()
            raise e

    @classmethod
    def count(cls, id=None, keyword_id=None):
        query = cls.session.query(func.count(cls.id))
        if id:
            query = query.filter(cls.id == id)
        if keyword_id:
            query = cls.session.query(func.count(cls.id)).join(JobKeywordModel,
                                                               and_(JobKeywordModel.keyword_id == keyword_id,
                                                                    cls.id == JobKeywordModel.job_id)) \
                .distinct()
        return query.scalar()

    @classmethod
    def list(cls, keyword_id=None, limit=None, offset=None):
        query = cls.session.query(cls)
        if keyword_id:
            query = cls.session.query(cls).join(JobKeywordModel,
                                                and_(JobKeywordModel.keyword_id == keyword_id,
                                                     cls.id == JobKeywordModel.job_id)).distinct()
        if limit:
            query = query.limit(limit=limit)
        if offset:
            query = query.offset(offset=offset)
        return query.all()

    @classmethod
    def get(cls, job_id):
        query = cls.session.query(cls).filter(cls.id == job_id)
        return query.one_or_none()
