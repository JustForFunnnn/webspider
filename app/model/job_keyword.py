# -*- coding: utf-8 -*-
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import INTEGER

from common.db import BaseModel


class JobKeywordModel(BaseModel):
    __tablename__ = 'job_keyword'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    job_id = Column(INTEGER, doc=u'工作 id')
    keyword_id = Column(INTEGER, doc=u'关键词 id')
    city_id = Column(INTEGER, doc=u'冗余:所在城市 id')

    @classmethod
    def list(cls, job_id=None):
        query = cls.session.query(cls)
        if job_id:
            query = query.filter(cls.job_id == job_id)
        return query.all()

    @classmethod
    def add(cls, job_id, keyword_id, city_id):
        job_keyword = cls(job_id=int(job_id), keyword_id=int(keyword_id), city_id=int(city_id))
        cls.session.merge(job_keyword)
        cls.session.commit()

    @classmethod
    def get_most_frequently_keywords(cls, limit):
        """
        获取出现频率最高的 n 个关键字
        :param limit: 限定前几个关键字
        :return: [(1,200),(2,100)....]  (keyword_id, count)
        """
        sql = text("""SELECT keyword.id, COUNT(*) AS count
                FROM job_keyword, keyword
                WHERE job_keyword.keyword_id = keyword.id
                GROUP BY job_keyword.keyword_id
                ORDER BY count DESC
                LIMIT :limit_count""")
        query = cls.session.execute(sql, {'limit_count': limit})
        return query.fetchall()
