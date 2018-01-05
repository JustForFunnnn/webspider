# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP, TINYINT

from webspider.models.base import BaseModel


class CompanyModel(BaseModel):
    __tablename__ = 'company'

    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    lagou_company_id = Column(INTEGER, nullable=False, doc='拉勾所使用的公司id')
    city_id = Column(INTEGER, nullable=False, doc=u'所在城市 id')
    shortname = Column(VARCHAR(64), nullable=False, doc=u'公司名称')
    fullname = Column(VARCHAR(128), nullable=False, doc=u'公司全称')
    finance_stage = Column(TINYINT, nullable=False, doc=u'融资阶段')
    size = Column(TINYINT, nullable=False, doc=u'公司规模')
    address = Column(VARCHAR(128), nullable=False, doc=u'公司地址')
    features = Column(VARCHAR(128), nullable=False, doc=u'公司特点')
    process_rate = Column(TINYINT, nullable=False, doc=u'简历处理率')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, doc=u'创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'最后更新时间')
