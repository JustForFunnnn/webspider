# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR

from webspider.models.base import BaseModel


class KeywordModel(BaseModel):
    __tablename__ = 'keyword'

    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(64), nullable=False, doc=u'关键词名称')
