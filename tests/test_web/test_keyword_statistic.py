# coding=utf-8
from datetime import datetime

from tornado.escape import json_decode

from tests.test_web.base import BaseHandlerTestCase
from webspider.utils.time_tools import datetime_to_timestamp

predictive_keyword_statistic_dict = {
    'educations': {'不限': 1, '大专': 2, '本科': 4, '硕士': 5, '博士': 6, 'unknown': 7},
    'city_jobs_count': {'北京': 8, '深圳': 9, '广州': 10},
    'salary': {'10k以下': 11, '11k-20k': 12, '21k-35k': 13, '36k-60k': 14, '61k以上': 15},
    'financing_stage': {'未融资': 16, '天使轮': 17, 'A轮': 18, 'B轮': 19, 'C轮': 20,
                        'D轮及以上': 21, '上市公司': 22, '不需要融资': 23, 'unknown': 24},
    'work_years': {'不限': 25, '应届毕业生': 26, '1年以下': 27, '1-3年': 28, '3-5年': 29,
                   '5-10年': 30, '10年以上': 31, 'unknown': 32},
    'per_day_jobs_count': [
        {
            'date': 20180128, 'all_city': 576, 'beijing': 198, 'guangzhou': 35, 'shenzhen': 93, 'shanghai': 80,
            'hangzhou': 41, 'chengdu': 26,
            'created_at': datetime_to_timestamp(datetime.strptime('2018-01-28 17:01:04', '%Y-%m-%d %H:%M:%S')),
            'updated_at': datetime_to_timestamp(datetime.strptime('2018-01-28 17:01:04', '%Y-%m-%d %H:%M:%S'))
        },
        {
            'date': 20180129, 'all_city': 580, 'beijing': 200, 'guangzhou': 36, 'shenzhen': 100, 'shanghai': 82,
            'hangzhou': 44, 'chengdu': 30,
            'created_at': datetime_to_timestamp(datetime.strptime('2018-01-28 17:01:04', '%Y-%m-%d %H:%M:%S')),
            'updated_at': datetime_to_timestamp(datetime.strptime('2018-01-28 17:01:04', '%Y-%m-%d %H:%M:%S'))
        }],
    'created_at': datetime_to_timestamp(datetime.strptime('2018-02-01 19:01:44', '%Y-%m-%d %H:%M:%S')),
    'updated_at': datetime_to_timestamp(datetime.strptime('2018-02-05 01:01:48', '%Y-%m-%d %H:%M:%S')),
}


class TestKeywordStatisticsApiHandler(BaseHandlerTestCase):

    def test_get(self):
        response = self.fetch_json('/api/statistics?keyword_name=python')
        self.assertDictEqual(predictive_keyword_statistic_dict, response)

    def test_get_when_error(self):
        response = self.get('/api/statistics')
        self.assertEqual(response.code, 404)
        predictive_response_content = {
            u"error": {
                u"message": u"请输入关键词",
                u"code": 4041,
                u"name": u"ResourceNotFoundWebException",
                u'data': '',
                u'debug_message': '',
            }
        }
        self.assertDictEqual(predictive_response_content, json_decode(response.body))

        response = self.get('/api/statistics?keyword_name=种田')
        self.assertEqual(response.code, 404)
        predictive_response_content = {
            u"error": {
                u"message": u"找不到该关键词",
                u"code": 4041,
                u"name": u"ResourceNotFoundWebException",
                u'data': '',
                u'debug_message': '',
            }
        }
        self.assertDictEqual(predictive_response_content, json_decode(response.body))

        response = self.get('/api/statistics?keyword_name=java')
        self.assertEqual(response.code, 404)
        predictive_response_content = {
            u"error": {
                u"message": u"暂无该关键词的统计结果",
                u"code": 4041,
                u"name": u"ResourceNotFoundWebException",
                u'data': '',
                u'debug_message': '',
            }
        }
        self.assertDictEqual(predictive_response_content, json_decode(response.body))


class TestKeywordStatisticsPageHandler(BaseHandlerTestCase):

    def test_get(self):
        response = self.get('/statistics?keyword_name=python')
        self.assertEqual(response.code, 200)

    def test_get_when_error(self):
        response = self.get('/api/statistics')
        self.assertEqual(response.code, 404)

        response = self.get('/api/statistics?keyword_name=种田')
        self.assertEqual(response.code, 404)

        response = self.get('/api/statistics?keyword_name=java')
        self.assertEqual(response.code, 404)
