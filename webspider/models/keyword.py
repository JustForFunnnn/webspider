# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP

from webspider.models.base import BaseModel


class KeywordModel(BaseModel):
    __tablename__ = 'keyword'

    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(64), nullable=False, doc=u'关键词名称')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, doc=u'创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'创建时间')
