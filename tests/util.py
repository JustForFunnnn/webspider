# coding=utf-8
import os

from sqlalchemy import text


def execute_sql_file(file_paths, db_session, predictive_db_name=''):
    if predictive_db_name:
        assert get_current_database_name(db_session) == predictive_db_name
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


def get_current_database_name(db_session):
    return db_session.execute('select database();').scalar()


def create_test_db(session, db_name='test_spider'):
    """转载数据库"""
    # 清除测试数据库
    drop_test_db(session)
    # 创建测试数据库
    session.execute("CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;".format(
        db_name=db_name))
    # 指定测试数据库 test_spider
    session.execute("USE {db_name};".format(db_name=db_name))

    path = os.path.dirname(__file__)
    # 创建表
    execute_sql_file(
        file_paths=[os.path.join(path, "schema.sql"), ],
        db_session=session,
        predictive_db_name=db_name
    )
    fixture_path = os.path.join(path, 'fixture')
    # 装载表数据
    fixture_file_paths = [os.path.join(fixture_path, file) for file in os.listdir(fixture_path)]
    execute_sql_file(
        file_paths=fixture_file_paths,
        db_session=session,
        predictive_db_name=db_name
    )
    assert get_current_database_name(session) == 'test_spider'


def drop_test_db(session, db_name='test_spider'):
    # 清除测试数据库
    session.execute("DROP DATABASE IF EXISTS {db_name};".format(db_name=db_name))
