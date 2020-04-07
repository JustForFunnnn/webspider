# coding=utf-8
from unittest import TestCase

from webspider.controllers import job_ctl


class TestJobController(TestCase):

    def test_get_salary_section(self):
        salary = '15k-25k'
        left, right = job_ctl.get_salary_section(salary)
        self.assertEqual(left, 15)
        self.assertEqual(right, 25)

        salary = '15k以上'
        left, right = job_ctl.get_salary_section(salary)
        self.assertEqual(left, 15)
        self.assertEqual(right, 20)

        salary = '15k以下'
        left, right = job_ctl.get_salary_section(salary)
        self.assertEqual(left, 10)
        self.assertEqual(right, 15)

        with self.assertRaises(ValueError):
            left, right = job_ctl.get_salary_section('15k30k')
