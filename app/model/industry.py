# -*- coding: utf-8 -*-
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR

from common.db import BaseModel


class IndustryModel(BaseModel):
    __tablename__ = 'industry'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(64), doc=u'行业名称')

    @classmethod
    def get(cls, name):
        query = cls.session.query(cls).filter(cls.name == name)
        return query.one_or_none()

    @classmethod
    def insert_if_not_exist(cls, name):
        """
        如果不存在 name == name　的数据库记录，则插入该条记录 
        :param name: 
        :return: 
        """
        sql = text("""INSERT INTO industry(name)
    SELECT :name AS name FROM dual
    WHERE NOT EXISTS
    (SELECT id FROM industry WHERE name = :name)""")
        cls.session.execute(sql, {'name': name})
        cls.session.commit()
