# coding: utf-8

import logging

from sqlalchemy import MetaData, inspect, func, text
from sqlalchemy.ext.declarative import declarative_base
from tornado.util import ObjectDict

from app.utils.sql import db_engine, Session
from app.utils.classproperty import classproperty

__all__ = ['BaseModel']

logger = logging.getLogger(__name__)

_Base = declarative_base()


class BaseModel(_Base):
    __abstract__ = True
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'extend_existing': True,
    }

    metadata = MetaData(bind=db_engine, reflect=True)

    @classproperty
    def session(self):
        return Session

    @classproperty
    def pk_name(cls):
        """主键名"""
        return inspect(cls).primary_key[0].name

    @classproperty
    def pk(cls):
        """表主键"""
        return getattr(cls, cls.pk_name)

    def dict(self):
        """sqlalchemy object -> dict"""
        columns = self.__table__.columns.keys()
        return ObjectDict((column, getattr(self, column)) for column in columns)

    @classmethod
    def add(cls, **values):
        """添加记录"""
        obj = cls(**values)
        cls.session.add(obj)
        cls.session.flush()
        return obj.id

    @classmethod
    def get_by_pk(cls, pk):
        """通过主键值获取记录"""
        query = cls.session.query(cls).filter(cls.pk == pk)
        return query.scalar()

    @classmethod
    def get_one(cls, filter=None, filter_by=None):
        """
        获取记录
        :param filter: apply the given filtering criterion to a copy of this Query,
        using SQL expressions.
        :param filter_by: apply the given filtering criterion to a copy of this Query,
        using keyword expressions as a dict.
        :return:
        """
        query = cls.session.query(cls)

        if filter is not None:
            query = query.filter(filter)
        if filter_by is not None:
            query = query.filter_by(**filter_by)

        return query.first()

    @classmethod
    def list(cls, filter=None, filter_by=None, order_by=None, offset=None, limit=None):
        """
        批量获取记录
        :param filter: apply the given filtering criterion to a copy of this Query,
        using SQL expressions.
        :param filter_by: apply the given filtering criterion to a copy of this Query,
        using keyword expressions as a dict.
        :param order_by: apply one or more ORDER BY criterion to the query and return
        the newly resulting ``Query``
        :param offset: Apply an ``OFFSET`` to the query and return the newly resulting
        ``Query``.
        :param limit: Apply a ``LIMIT`` to the query and return the newly resulting
        ``Query``.
        :return:
        """
        query = cls.session.query(cls)

        if filter is not None:
            query = query.filter(filter)
        if filter_by is not None:
            query = query.filter_by(**filter_by)
        if order_by is not None:
            if isinstance(order_by, str):
                order_by = text(order_by)
            query = query.order_by(order_by)
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)

        result = query.all()

        return result

    @classmethod
    def count(cls, filter=None, filter_by=None):
        """

        :param filter: apply the given filtering criterion to a copy of this Query,
        using SQL expressions.
        :param filter_by: apply the given filtering criterion to a copy of this Query,
        using keyword expressions as a dict.
        :return:
        """
        query = cls.session.query(func.count(cls.pk))

        if filter is not None:
            query = query.filter(filter)
        if filter_by is not None:
            query = query.filter_by(**filter_by)

        return query.scalar()

    @classmethod
    def update(cls, filter=None, filter_by=None, values=None):
        """更新数据
        :param filter: apply the given filtering criterion to a copy of this Query,
        using SQL expressions.
        :param filter_by: apply the given filtering criterion to a copy of this Query,
        using keyword expressions as a dict.
        :param values: values to update
        :return: type: int, affected rows
        """
        query = cls.session.query(cls)

        if filter is not None:
            query = query.filter(filter)

        if filter_by is not None:
            query = query.filter_by(**filter_by)

        affect_rows = query.update(values)
        return affect_rows

    @classmethod
    def update_by_pk(cls, pk, values):
        """主键更新数据

        :param pk: 主键值
        :param values: 要更新的值，key=value 形式
        :return: 返回变更的行数
        """
        return cls.update(filter=(cls.pk == pk), values=values)
