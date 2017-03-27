# coding=utf-8
import re
import time
import random

from sqlalchemy import text

from common import constants


def update_salary_dict(salary_dict, start, end):
    if len(salary_dict) == 0:
        salary_dict = {i: 0 for i in range(0, 111)}
    for index in range(start, end + 1):
        salary_dict[index] += 1
    return salary_dict


def get_salary_section(string):
    """
    e.g:
    15k-25k  ->  (15, 25)
    15k以上  ->  (15, 20)
    15k以下  ->  (10, 15)
    :param string: 15k-25k
    :return: 15,25
    """
    pattern = r'K|k|以上|以下'
    replace_char = ''

    if string.find('-') != -1:
        string = re.sub(pattern=pattern, repl=replace_char, string=string)
        start, end = string.split('-')
    elif string.endswith('以下'):
        string = re.sub(pattern=pattern, repl=replace_char, string=string)
        start, end = int(string) - 5 if int(string) - 5 >= 0 else 1, string
    elif string.endswith('以上'):
        string = re.sub(pattern=pattern, repl=replace_char, string=string)
        start, end = string, int(string) + 5
    else:
        raise Exception('error salary' + string)

    return int(start), int(end)


def reverse_dict(old_dict):
    return {value: key for (key, value) in old_dict.items()}


def execute_sql_file(file_paths, db_session):
    """
    执行 sql 文件
    :param file_paths: .sql 文件的 path 
    :param db_session: 
    :return: 
    """
    # Open the .sql file
    for file_path in file_paths:
        sql_file = open(file_path, 'r')

        # Create an empty command string
        sql_command = ''

        # Iterate over all lines in the sql file
        for line in sql_file:
            # Ignore comented lines
            if not line.startswith('--'):
                # Append line to the command string
                sql_command += line.strip('\n')

                # If the command string ends with ';', it is a full statement
                if sql_command.endswith(';'):
                    # Try to execute statemente and commit it
                    db_session.execute(text(sql_command))
                    db_session.commit()
                    sql_command = ''


def crawler_sleep():
    """爬虫休眠"""
    time.sleep(random.uniform(constants.MIN_SLEEP_TIME, constants.MAX_SLEEP_TIME))
