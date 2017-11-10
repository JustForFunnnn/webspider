# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER

from common.db import BaseModel


class JobKeywordModel(BaseModel):
    __tablename__ = 'job_keyword'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    job_id = Column(INTEGER, doc=u'工作 id')
    keyword_id = Column(INTEGER, doc=u'关键词 id')
    city_id = Column(INTEGER, doc=u'冗余:所在城市 id')

    @classmethod
    def list(cls, job_id=None):
        query = cls.session.query(cls)
        if job_id:
            query = query.filter(cls.job_id == job_id)
        return query.all()

    @classmethod
    def add(cls, job_id, keyword_id, city_id):
        job_keyword = cls(job_id=int(job_id), keyword_id=int(keyword_id), city_id=int(city_id))
        cls.session.merge(job_keyword)
        cls.session.flush()
