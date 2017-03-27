# coding=utf-8
import logging

from tests import BaseTestCase
from app.model.job import JobModel


class JobModelTestCase(BaseTestCase):
    def test_get_job(self):
        job = JobModel.get(job_id=6814)
        self.assertEqual(job.id, 6814)
        self.assertEqual(job.title, 'web前端')

    def test_list_job(self):
        jobs = JobModel.list()
        self.assertEqual(len(jobs), 2)
        jobs = JobModel.list(keyword_id=100)
        self.assertEqual(len(jobs), 2)

    def test_add_job(self):
        data = {
            'id': 1001,
            'title': '招聘绅士hentai',
            'work_year': 3,
            'city_id': 2,
            'company_id': 11,
            'department': '二次元部门',
            'salary': '60k-100k',
            'education': 2,
            'description': '这是JD这是JD这是JD这是JD这是JD这是JD',
            'advantage': '有妹子',
            'job_nature': 2,
            'created_at': 1494957220,
        }
        JobModel.add(**data)
        jobs = JobModel.list()
        self.assertEqual(len(jobs), 3)
        job = JobModel.get(job_id=1001)
        for (key, value) in data.items():
            self.assertEqual(getattr(job, key), value)

    def test_count_job(self):
        count = JobModel.count()
        self.assertEqual(count, 2)
        count = JobModel.count(keyword_id=100)
        self.assertEqual(count, 2)
