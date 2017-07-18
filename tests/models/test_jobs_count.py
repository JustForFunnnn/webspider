# coding=utf-8
from tests import BaseTestCase
from app.model.jobs_count import JobsCountModel


class JobsCountModelTestCase(BaseTestCase):
    def test_list_jobs_count(self):
        jobs_count = JobsCountModel.list(keyword_id=100)
        self.assertEqual(len(jobs_count), 4)
        self.assertEqual(jobs_count[0].date, 1500134400)

        jobs_count = JobsCountModel.list(keyword_id=100, use_desc=False)
        self.assertEqual(len(jobs_count), 4)
        self.assertEqual(jobs_count[0].date, 1499616000)

        jobs_count = JobsCountModel.list(keyword_id=100, start_time=1499702400, end_time=1499875200,
                                         order_key='all_city')
        self.assertEqual(len(jobs_count), 2)
        self.assertEqual(jobs_count[0].all_city, 2540)

        jobs_count = JobsCountModel.list(keyword_id=100, start_time=1499702400, end_time=1499875200,
                                         order_key='all_city', use_desc=False)
        self.assertEqual(len(jobs_count), 2)
        self.assertEqual(jobs_count[0].all_city, 2477)

    def test_add_jobs_count(self):
        data = {
            'date': 6815,
            'keyword_id': 112,
            'all_city': 1024,
            'beijing': 500,
            'guangzhou': 200,
            'shenzhen': 200,
            'shanghai': 100,
            'hangzhou': 50,
            'chengdu': 50,
        }
        JobsCountModel.add(**data)
        jobs_count = JobsCountModel.list()
        self.assertEqual(len(jobs_count), 6)
        jobs_count = JobsCountModel.list(keyword_id=112)
        self.assertEqual(len(jobs_count), 1)
        for (key, value) in data.items():
            self.assertEqual(getattr(jobs_count[0], key), value)
