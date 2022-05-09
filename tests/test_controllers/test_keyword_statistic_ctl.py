# coding=utf-8
from tests import BaseTestCase
from webspider.controllers import keyword_statistic_ctl
from webspider.models import JobModel
from webspider.constants import EDUCATION_REQUEST_DICT, WORK_YEARS_REQUEST_DICT


class TestKeywordStatisticController(BaseTestCase):
    def test_get_salary_statistic(self):
        test_jobs_model = [JobModel(salary='5k-9k'), JobModel(salary='10-15k'), JobModel(salary='15k-20k'),
                           JobModel(salary='16-18k'), JobModel(salary='20k-30k'), JobModel(salary='30k-35k'),
                           JobModel(salary='20k以上'), JobModel(salary='60k-100k'), JobModel(salary='40k-42k')]
        salary_statistic = keyword_statistic_ctl.get_salary_statistic(test_jobs_model)
        self.assertDictEqual(salary_statistic, {
            '10k及以下': 2,
            '11k-20k': 5,
            '21k-35k': 3,
            '36k-60k': 2,
            '61k以上': 1,
        })

    def test_get_finance_stage_statistic(self):
        test_jobs_model = [JobModel(company_id=1), JobModel(company_id=2), JobModel(company_id=3)]
        finance_stage_statistic = keyword_statistic_ctl.get_finance_stage_statistic(test_jobs_model)
        self.assertDictEqual(finance_stage_statistic, {
            '未融资': 2,
            'A轮': 1,
        })

    def test_get_educations_statistic(self):
        test_jobs_model = [JobModel(education=EDUCATION_REQUEST_DICT['大专']),
                           JobModel(education=EDUCATION_REQUEST_DICT['本科']),
                           JobModel(education=EDUCATION_REQUEST_DICT['本科'])]
        educations_statistic = keyword_statistic_ctl.get_educations_statistic(test_jobs_model)
        self.assertDictEqual(educations_statistic, {
            '本科': 2,
            '大专': 1,
        })

    def test_get_work_years_statistic(self):
        test_jobs_model = [JobModel(work_year=WORK_YEARS_REQUEST_DICT['应届毕业生']),
                           JobModel(work_year=WORK_YEARS_REQUEST_DICT['应届毕业生']),
                           JobModel(work_year=WORK_YEARS_REQUEST_DICT['1-3年'])]
        work_years_statistic = keyword_statistic_ctl.get_work_years_statistic(test_jobs_model)
        self.assertDictEqual(work_years_statistic, {
            '应届毕业生': 2,
            '1-3年': 1,
        })

    def test_get_city_jobs_count_statistic(self):
        test_jobs_model = [JobModel(city_id=2), JobModel(city_id=2), JobModel(city_id=2), JobModel(city_id=2),
                           JobModel(city_id=3), JobModel(city_id=3), JobModel(city_id=3),
                           JobModel(city_id=4), JobModel(city_id=4)]
        sorted_city_jobs_count_statistic = keyword_statistic_ctl.get_city_jobs_count_statistic(test_jobs_model)
        self.assertDictEqual(sorted_city_jobs_count_statistic, {
            '北京': 4,
            '上海': 3,
            '广州': 2,
        })

        sorted_city_jobs_count_statistic = keyword_statistic_ctl.get_city_jobs_count_statistic(test_jobs_model, 2)
        self.assertDictEqual(sorted_city_jobs_count_statistic, {
            '北京': 4,
            '上海': 3
        })
