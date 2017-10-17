# coding=utf-8
import logging

import redis
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from common import config

LOGGER = logging.getLogger(__name__)
# isolation_level 读取没提交的数据 避免脏数据
DB_engine = create_engine(config.DB_CONF['host'], isolation_level="READ UNCOMMITTED", pool_recycle=3600)
_BaseModel = declarative_base()
_Session = sessionmaker(bind=DB_engine)


class BaseModel(_BaseModel):
    __abstract__ = True
    __metadata__ = MetaData(bind=DB_engine)
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'extend_existing': True,
    }
    session = _Session(autocommit=False)


redis_pool = redis.ConnectionPool(host=config.REDIS_CONF['host'],
                                  port=config.REDIS_CONF['port'])
redis_instance = redis.Redis(connection_pool=redis_pool)
