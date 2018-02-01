# coding=utf-8
from datetime import datetime
from unittest import TestCase

from webspider.utils.time_tools import (datetime_to_timestamp, timestamp_to_datetime, timestamp_to_datetime_str)


class TestUtilTimeTools(TestCase):
    def test_datetime_to_timestamp(self):
        datetime_obj = datetime.strptime('2017-05-10', '%Y-%m-%d')
        timestamp = datetime_to_timestamp(datetime_obj)
        self.assertEqual(1494345600, timestamp)

    def test_timestamp_to_datetime(self):
        timestamp = 1494345600
        datetime_obj = timestamp_to_datetime(timestamp=timestamp)
        self.assertEqual(datetime_obj.isoformat(), '2017-05-10T00:00:00')

    def test_timestamp_to_datetime_str(self):
        timestamp = 1494345600
        datetime_str = timestamp_to_datetime_str(ts=timestamp)
        self.assertEqual(datetime_str, '2017-05-10')

        timestamp = 1517485617
        datetime_str = timestamp_to_datetime_str(ts=timestamp, time_format='%Y/%m/%d %H:%M:%S')
        self.assertEqual(datetime_str, '2018/02/01 19:46:57')
