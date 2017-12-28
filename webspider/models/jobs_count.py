# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, TIMESTAMP

from common.db import BaseModel


class JobsQuantityModel(BaseModel):
    __tablename__ = 'job_quantity'

    date = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    keyword_id = Column(INTEGER, nullable=False, primary_key=True)
    all_city = Column(INTEGER, nullable=False, default=0, doc=u'全国岗位数量')
    beijing = Column(INTEGER, nullable=False, default=0, doc=u'北京岗位数量')
    guangzhou = Column(INTEGER, nullable=False, default=0, doc=u'广州岗位数量')
    shenzhen = Column(INTEGER, nullable=False, default=0, doc=u'深圳岗位数量')
    shanghai = Column(INTEGER, nullable=False, default=0, doc=u'上海岗位数量')
    hangzhou = Column(INTEGER, nullable=False, default=0, doc=u'杭州岗位数量')
    chengdu = Column(INTEGER, nullable=False, default=0, doc=u'成都岗位数量')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, doc=u'创建时间')
