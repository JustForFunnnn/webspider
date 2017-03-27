# -*- coding: utf-8 -*-
import time

from sqlalchemy import Column, func
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TEXT, TINYINT

from common.db import BaseModel


class CompanyModel(BaseModel):
    __tablename__ = 'company'

    id = Column(INTEGER, primary_key=True)
    city_id = Column(INTEGER, doc=u'所在城市 id')
    shortname = Column(VARCHAR(64), doc=u'公司名称')
    fullname = Column(VARCHAR(128), doc=u'公司全称')
    finance_stage = Column(TINYINT, doc=u'融资阶段')
    advantage = Column(VARCHAR(128), doc=u'公司优势')
    size = Column(TINYINT, doc=u'公司规模')
    address = Column(VARCHAR(256), doc=u'公司地址')
    features = Column(VARCHAR(128), doc=u'公司特点')
    introduce = Column(TEXT, doc=u'公司简介')
    process_rate = Column(TINYINT, doc=u'简历处理率')
    updated_at = Column(INTEGER, default=time.time, onupdate=time.time, doc=u'最后更新时间')

    @classmethod
    def add(cls, id, shortname, fullname, city_id, finance_stage=0, process_rate=0, features='', introduce='',
            address='', advantage='', size=0):
        company = cls(id=id, shortname=shortname, fullname=fullname, finance_stage=int(finance_stage),
                      city_id=int(city_id), process_rate=process_rate, features=features, introduce=introduce,
                      address=address, advantage=advantage, size=int(size))
        try:
            cls.session.merge(company)
            cls.session.commit()
        except InvalidRequestError as e:
            cls.session.rollback()
            raise e

    @classmethod
    def list(cls, ids=None, city_id=None, limit=None):
        query = cls.session.query(cls).order_by(cls.updated_at.desc())
        if city_id:
            query = query.filter(cls.city_id == city_id)
        if limit:
            query = query.limit(limit=limit)
        if ids:
            query = query.filter(cls.id.in_(ids))
        return query.all()

    @classmethod
    def update(cls, id, update_attr):
        cls.session.query(cls).filter_by(id=id).update(update_attr)
        cls.session.commit()

    @classmethod
    def count(cls, id=None):
        query = cls.session.query(func.count(cls.id))
        if id:
            query = query.filter(cls.id == id)
        return query.scalar()
