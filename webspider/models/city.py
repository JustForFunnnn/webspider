# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP, DATE

from common.db import BaseModel


class CityModel(BaseModel):
    __tablename__ = 'city'

    id = Column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
    name = Column(VARCHAR(64), nullable=False, doc=u'城市名')

    @classmethod
    def list(cls):
        query = cls.session.query(cls)
        return query.all()

    @classmethod
    def add(cls, id, name):
        city = cls(id=id, name=name)
        cls.session.merge(city)
        cls.session.flush()

    @classmethod
    def get(cls, id=None, name=None):
        query = cls.session.query(cls)
        if name:
            query = query.filter(cls.name == name)
        if id:
            query = query.filter(cls.id == id)
        return query.one_or_none()
