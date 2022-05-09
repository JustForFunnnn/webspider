# coding=utf-8
from unittest import TestCase, mock

from webspider.utils.http_tools import generate_http_request_headers, requests_get, requests_post


class TestUtilHttpTools(TestCase):
    def test_generate_http_request_headers(self):
        header = generate_http_request_headers()
        self.assertTrue(isinstance(header, dict))

        header = generate_http_request_headers(referer='https://www.zhihu.com')
        self.assertEqual(header['Referer'], 'https://www.zhihu.com')

    @mock.patch('requests.get')
    def test_request_get(self, mock_get):
        mock_get.return_value = '200'
        response = requests_get(url='https://baidu.com', need_sleep=False)
        self.assertEqual(response, '200')

    @mock.patch('requests.post')
    def test_request_post(self, mock_post):
        mock_post.return_value = '200'
        response = requests_post(url='https://baidu.com', need_sleep=False)
        self.assertEqual(response, '200')
