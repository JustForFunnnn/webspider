# coding: utf-8
import time
import datetime as datetime


def datetime_to_timestamp(datetime_obj):
    return int(time.mktime(datetime_obj.timetuple()))


def timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


def timestamp_to_datetime_str(ts, time_format=None):
    """
    时间戳转化为日期字符串(1476547200->'2016-10-16')
    :param ts: 时间戳
    :param time_format: '日期格式'
    :return: 日期字符串
    """
    if time_format is None or time_format == '':
        time_format = '%Y-%m-%d'
    ts = time.localtime(float(ts))
    return time.strftime(time_format, ts)
