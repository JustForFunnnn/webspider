# coding=utf-8
from datetime import datetime
from unittest import TestCase

from webspider.utils.time_tools import (datetime_to_timestamp, timestamp_to_datetime, timestamp_to_datetime_str)


class TestUtilTimeTools(TestCase):
    def test_datetime_to_timestamp(self):
        datetime_obj = datetime(year=2017, month=5, day=10)
        timestamp = datetime_to_timestamp(datetime_obj)
        self.assertEqual(int(datetime_obj.timestamp()), timestamp)

    def test_timestamp_to_datetime(self):
        timestamp = int(datetime(year=2017, month=5, day=10).timestamp())
        datetime_obj = timestamp_to_datetime(timestamp=timestamp)
        self.assertEqual(datetime_obj.isoformat(), '2017-05-10T00:00:00')

    def test_timestamp_to_datetime_str(self):
        timestamp = int(datetime(year=2017, month=5, day=10).timestamp())
        datetime_str = timestamp_to_datetime_str(ts=timestamp)
        self.assertEqual(datetime_str, '2017-05-10')

        timestamp = int(datetime(year=2018, month=2, day=1, hour=19, minute=46, second=57).timestamp())
        datetime_str = timestamp_to_datetime_str(ts=timestamp, time_format='%Y/%m/%d %H:%M:%S')
        self.assertEqual(datetime_str, '2018/02/01 19:46:57')
