# -*- coding: utf-8 -*-
import re


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
        raise ValueError('error salary' + string)

    return int(start), int(end)
