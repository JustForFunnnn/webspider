# coding: utf-8
# import time
# from unittest import TestCase
#
# from app.utils.time_tools import (timestamp2string, date2timestamp, job_date2timestamp)

#
# class TimeToolsTestCase(TestCase):
#     def test_date2timestamp(self):
#         date_string = '2017-05-10'
#         timestamp = date2timestamp(date_string=date_string)
#         self.assertEqual(1494345600, timestamp)
#
#         date_string = '2017-05-10 12:00:01'
#         timestamp = date2timestamp(date_string=date_string, date_format='%Y-%m-%d %H:%M:%S')
#         self.assertEqual(1494388801, timestamp)
#
#     def test_timestamp2string(self):
#         timestamp = 1494345600
#         timestamp = timestamp2string(timestamp=timestamp)
#         self.assertEqual('2017-05-10', timestamp)
#
#         timestamp = 1494388801
#         timestamp = timestamp2string(timestamp=timestamp, date_format='%Y-%m-%d %H:%M:%S')
#         self.assertEqual('2017-05-10 12:00:01', timestamp)
#
#     def test_job_date2timestamp(self):
#         date_str = '2017-11-12'
#         timestamp = job_date2timestamp(time_string=date_str)
#         self.assertEqual(timestamp, 1510416000)
#
#         now_date_str = timestamp2string(timestamp=time.time())
#         date_str = now_date_str + ' 12:01'
#         right_timestamp = date2timestamp(date_string=date_str, date_format='%Y-%m-%d %H:%M')
#         timestamp = job_date2timestamp(time_string='12:01')
#         self.assertEqual(timestamp, right_timestamp)
