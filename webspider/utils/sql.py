# coding: utf-8
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from webspider import setting

__all__ = ['get_session', 'remove_sessions', 'db_engine']

logger = logging.getLogger(__name__)

db_engine = create_engine(
    setting.MYSQL_CONF['connect_string'],
    echo=False, max_overflow=48,
    pool_timeout=0, pool_recycle=3600,
    logging_name='sql')

_session = scoped_session(sessionmaker(bind=db_engine, autocommit=True, autoflush=True))


def get_session():
    return _session


def remove_sessions():
    _session.remove()
