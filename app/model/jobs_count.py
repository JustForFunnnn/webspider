# -*- coding: utf-8 -*-
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR

from common.db import BaseModel


class JobsCountModel(BaseModel):
    __tablename__ = 'jobs_count'

    date = Column(INTEGER, primary_key=True)
    keyword_id = Column(INTEGER, primary_key=True)
    all_city = Column(INTEGER, default=0, doc=u'全国岗位数量')
    beijing = Column(INTEGER, default=0, doc=u'北京岗位数量')
    guangzhou = Column(INTEGER, default=0, doc=u'广州岗位数量')
    shenzhen = Column(INTEGER, default=0, doc=u'深圳岗位数量')
    shanghai = Column(INTEGER, default=0, doc=u'上海岗位数量')
    hangzhou = Column(INTEGER, default=0, doc=u'杭州岗位数量')
    chengdu = Column(INTEGER, default=0, doc=u'成都岗位数量')

    @classmethod
    def add(cls, date, keyword_id, all_city, beijing, guangzhou, shenzhen, shanghai, hangzhou, chengdu):
        jobs_count = cls(date=int(date), keyword_id=int(keyword_id), all_city=int(all_city), beijing=int(beijing),
                         guangzhou=int(guangzhou), shenzhen=int(shenzhen), shanghai=int(shanghai),
                         hangzhou=int(hangzhou), chengdu=int(chengdu))
        cls.session.merge(jobs_count)
        cls.session.commit()

    @classmethod
    def list(cls, keyword_id=None, start_time=None, end_time=None, order_key='date', sort_by='desc'):
        query = cls.session.query(cls)
        if keyword_id:
            query = query.filter(cls.keyword_id == keyword_id)
        if start_time:
            query = query.filter(cls.date >= start_time)
        if end_time:
            query = query.filter(cls.date <= end_time)
        if order_key:
            try:
                order_key = getattr(cls, order_key)
            except:
                raise Exception(u'illegal order key: {}'.format(order_key))
            if sort_by == 'desc':
                query = query.order_by(order_key.desc())
            else:
                query = query.order_by(order_key.asc())
        return query.all()
