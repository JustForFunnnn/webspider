# -*- coding: utf-8 -*-
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR

from common.db import BaseModel


class KeywordModel(BaseModel):
    __tablename__ = 'keyword'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(64), doc=u'关键词名称')

    @classmethod
    def get(cls, name):
        query = cls.session.query(cls).filter(cls.name == name)
        return query.one_or_none()

    @classmethod
    def list(cls, name=None):
        query = cls.session.query(cls)
        if name:
            query = query.filter(cls.name.like('%' + name + '%'))
        return query.all()

    @classmethod
    def insert_if_not_exist(cls, name):
        """
        如果不存在 name == name　的数据库记录，则插入该条记录 
        :param name: 
        :return: 
        """
        sql = text("""INSERT INTO keyword(name)
SELECT :name as name FROM dual
WHERE NOT EXISTS
(SELECT id FROM keyword WHERE name = :name)""")
        cls.session.execute(sql, {'name': name})
        cls.session.commit()

    @classmethod
    def get_most_frequently_keywords(cls, limit=10):
        """
        获取出现频率最高的 n 个关键字
        :param limit: 限定前几个关键字
        :return:
        """
        sql = text("""SELECT keyword.id, keyword.name, COUNT(*) AS count
                FROM keyword, job_keyword
                WHERE keyword.id = job_keyword.keyword_id 
                GROUP BY keyword.id, keyword.name
                ORDER BY count DESC
                LIMIT :limit_count""")
        query = cls.session.execute(sql, {'limit_count': limit})
        result = query.fetchall()
        keywords = []
        for row in result:
            keyword = KeywordModel(id=row[0], name=row[1])
            keyword.times = row[2]
            keywords.append(keyword)
        return keywords
