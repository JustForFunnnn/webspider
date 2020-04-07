# coding=utf-8
from tests import BaseTestCase
from webspider.controllers import job_keyword_ctl


class TestJobKeywordController(BaseTestCase):
    def test_get_most_frequently_keyword_ids(self):
        keyword_ids = job_keyword_ctl.get_most_frequently_keyword_ids()
        self.assertEqual(keyword_ids, [100, 101, 102])

        keyword_ids = job_keyword_ctl.get_most_frequently_keyword_ids(limit=2)
        self.assertEqual(keyword_ids, [100, 101])

        keyword_ids = job_keyword_ctl.get_most_frequently_keyword_ids(offset=1)
        self.assertEqual(keyword_ids, [101, 102])

        keyword_ids = job_keyword_ctl.get_most_frequently_keyword_ids(limit=1, offset=1)
        self.assertEqual(keyword_ids, [101])
