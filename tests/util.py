# coding=utf-8
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
