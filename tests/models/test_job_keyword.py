# coding=utf-8
from tests import BaseTestCase
from app.model.job_keyword import JobKeywordModel


class JobKeywordModelTestCase(BaseTestCase):
    def test_list_job_keyword(self):
        job_kyewords = JobKeywordModel.list()
        self.assertEqual(len(job_kyewords), 3)

    def test_add_job_keyword(self):
        data = {
            'job_id': 6815,
            'city_id': 2,
            'keyword_id': 111
        }
        JobKeywordModel.add(**data)
        job_kyewords = JobKeywordModel.list()
        self.assertEqual(len(job_kyewords), 4)
        job_kyewords = JobKeywordModel.list(job_id=6815)
        self.assertEqual(len(job_kyewords), 1)
        for (key, value) in data.items():
            self.assertEqual(getattr(job_kyewords[0], key), value)

    def test_get_most_frequently_keywords(self):
        keyword_counts = JobKeywordModel.get_most_frequently_keywords(limit=10)
        self.assertEqual(keyword_counts[0], (100, 2))
        self.assertEqual(keyword_counts[1], (101, 1))
