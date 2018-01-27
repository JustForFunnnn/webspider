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


def execute_sql_file(file_paths, db_session):
    """
    执行 sql 文件
    :param file_paths: .sql 文件的 path
    :param db_session:
    :return:
    """
    for file_path in file_paths:
        sql_file = open(file_path, 'r')

        sql_command = ''

        for line in sql_file:
            if not line.startswith('--'):
                sql_command += line.strip('\n')

                if sql_command.endswith(';'):
                    db_session.execute(text(sql_command))
                    db_session.flush()
                    sql_command = ''
