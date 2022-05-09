# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP, TINYINT

from webspider import constants
from webspider.models.base import BaseModel


class CompanyModel(BaseModel):
    __tablename__ = 'company'

    id = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)
    lg_company_id = Column(INTEGER, nullable=False, doc='所使用的公司id')
    city_id = Column(INTEGER, nullable=False, doc=u'所在城市 id')
    shortname = Column(VARCHAR(64), nullable=False, doc=u'公司名称')
    fullname = Column(VARCHAR(128), nullable=False, doc=u'公司全称')
    finance_stage = Column(TINYINT, nullable=False, doc=u'融资阶段')
    size = Column(TINYINT, nullable=False, doc=u'公司规模')
    address = Column(VARCHAR(128), nullable=False, doc=u'公司地址')
    features = Column(VARCHAR(128), nullable=False, doc=u'公司特点')
    process_rate = Column(TINYINT, nullable=False, doc=u'简历处理率')
    introduce = Column(VARCHAR(constants.COMPANY_INTRODUCE_MAX_LEN), nullable=False, doc=u'公司简介')
    advantage = Column(VARCHAR(constants.COMPANY_ADVANTAGE_MAX_LEN), nullable=False, doc=u'公司优势')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, doc=u'创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now,
                        onupdate=datetime.now, doc=u'最后更新时间')
