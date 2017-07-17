# coding: utf-8

import time
import datetime as dt

from common import constants


def get_date_begin_by_timestamp(timestamp=None, after_days=0):
    """
    获取时间戳对应的日期的开始时间
    :param timestamp: 时间戳
    :param after_days: 相对于当天后 n 天的时间戳 可以为负数
    :return:
    """
    if timestamp is None:
        timestamp = time.time()
    date_string = time.strftime('%Y-%m-%d', time.localtime(timestamp))
    strut_time = time.strptime(date_string, '%Y-%m-%d')
    return int(time.mktime(strut_time) + constants.SECONDS_OF_DAY * after_days)


def date2timestamp(date_string, date_format='%Y-%m-%d'):
    """
    转换 string 格式为 timestamp
    :param date_string: 要转换的日期字符串
    :param date_format: 日期格式
    :return: timestamp
    """
    # C-level APIs not support key-arguments
    datetime = dt.datetime.strptime(date_string, date_format)
    if not datetime:
        raise ValueError(u'{} for format "{}" not valid'.format(date_string, date_format))
    return int(time.mktime(datetime.timetuple()))


def timestamp2string(timestamp, date_format='%Y-%m-%d'):
    """
    转换 timestamp 为 date_string
    :param timestamp: 要转换的时间戳
    :param date_format: 转换的格式
    :return: date_string
    """
    dtime = dt.datetime.fromtimestamp(timestamp)
    return dtime.strftime(date_format)


def job_date2timestamp(time_string):
    """
    抓取公司下招聘职位时 时间处理(会同时出现'2017-11-12' or '12:01' 两种情况)
    把传入的抓取结果转化为时间戳
    :param time_string:
    :return:
    """
    date, hour_min_seconds = None, None
    if time_string.find(':') != -1:
        hour_min_seconds = time_string
    else:
        date = time_string
    if date is None:
        date = dt.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')
    if hour_min_seconds is None:
        hour_min_seconds = '00:00'
    return date2timestamp(date_string=date + ' ' + hour_min_seconds, date_format='%Y-%m-%d %H:%M')
