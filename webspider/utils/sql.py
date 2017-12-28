# coding: utf-8

import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from webspider import setting

logger = logging.getLogger(__name__)

db_engine = create_engine(
    setting.MYSQL_CONF['host'], echo=False,
    pool_size=2, max_overflow=48,
    pool_timeout=0, pool_recycle=3600,
    logging_name='mysql-sql')

Session = scoped_session(sessionmaker(bind=db_engine, autocommit=True, autoflush=True))
