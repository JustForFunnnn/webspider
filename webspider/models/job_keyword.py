# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER

from webspider.models.base import BaseModel


class JobKeywordModel(BaseModel):
    __tablename__ = 'job_keyword'

    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    job_id = Column(INTEGER, nullable=False, doc=u'工作 id')
    keyword_id = Column(INTEGER, nullable=False, doc=u'关键词 id')
