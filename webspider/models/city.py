# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP

from webspider.models.base import BaseModel


class CityModel(BaseModel):
    __tablename__ = 'city'

    id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    name = Column(VARCHAR(64), nullable=False, doc=u'城市名')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, doc=u'创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'最后更新时间')
