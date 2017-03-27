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
