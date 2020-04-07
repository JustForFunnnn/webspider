# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP

from webspider.models.base import BaseModel


class JobKeywordModel(BaseModel):
    __tablename__ = 'job_keyword'

    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    job_id = Column(INTEGER, nullable=False, doc=u'职位 id')
    keyword_id = Column(INTEGER, nullable=False, doc=u'关键词 id')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, doc=u'创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'创建时间')
