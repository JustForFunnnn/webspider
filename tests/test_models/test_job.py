# coding=utf-8
from datetime import datetime

from sqlalchemy import and_

from tests import BaseTestCase
from webspider.models import JobModel, CityModel

test_job_dict = dict(id=1,
                     lg_job_id=10001,
                     city_id=2,
                     company_id=1,
                     title='高级前端开发工程师',
                     work_year=5,
                     department='贝壳金控交易研发部-交易前端组招聘',
                     salary='15k-30k',
                     education=3,
                     nature=1,
                     description='职位介绍A',
                     advantage='15薪,工作居住证,六险一金,双休',
                     created_at=datetime.strptime('2018-01-29 19:11:33', '%Y-%m-%d %H:%M:%S'),
                     updated_at=datetime.strptime('2018-01-30 17:22:30', '%Y-%m-%d %H:%M:%S'))


class TestJobModel(BaseTestCase):
    def test_pk_name(self):
        self.assertEqual(JobModel.pk_name, 'id')

    def test_pk(self):
        self.assertEqual(JobModel.pk, JobModel.id)

    def test_model_instance_to_dict(self):
        job = JobModel.get_by_pk(pk=1).dict()
        self.assertTrue(isinstance(job, dict))
        self.assertDictEqual(job, test_job_dict)

    def test_get_by_pk(self):
        job = JobModel.get_by_pk(pk=1)
        self.assertDictEqual(job.dict(), test_job_dict)

    def test_count(self):
        jobs_count = JobModel.count()
        self.assertEqual(jobs_count, 3)

        jobs_count = JobModel.count(filter_by={'city_id': 4})
        self.assertEqual(jobs_count, 2)

        jobs_count = JobModel.count(filter=(and_(JobModel.city_id == 4, JobModel.company_id == 3)))
        self.assertEqual(jobs_count, 1)

        jobs_count = JobModel.count(filter=(JobModel.id == 1))
        self.assertEqual(jobs_count, 1)

    def test_is_exist(self):
        is_exist = JobModel.is_exist(filter=(JobModel.id == 1))
        self.assertEqual(is_exist, True)

    def test_add(self):
        to_add_data_dict = dict(lg_job_id=10004,
                                city_id=3,
                                company_id=1,
                                title='Python 开发工程师',
                                work_year=5,
                                department='吖吖项目组',
                                salary='15k-35k',
                                education=2,
                                nature=1,
                                description='职位介绍D',
                                advantage='16薪,工作居住证,六十八险一金,双休', )
        job_id = JobModel.add(**to_add_data_dict)
        self.assertTrue(job_id > 0)
        job = JobModel.get_by_pk(pk=job_id)
        self.assertDictContainsSubset(to_add_data_dict, job.dict())

    def test_get_one(self):
        job = JobModel.get_one(filter_by={'id': 1})
        self.assertDictEqual(job.dict(), test_job_dict)

        job = JobModel.get_one(filter=(JobModel.id == 1))
        self.assertDictEqual(job.dict(), test_job_dict)

    def test_list(self):
        # test list
        jobs = JobModel.list()
        self.assertEqual(len(jobs), 3)
        self.assertDictEqual(jobs[0].dict(), test_job_dict)

        # test list limit
        jobs = JobModel.list(limit=1)
        self.assertEqual(len(jobs), 1)

        # test list offset
        jobs = JobModel.list(offset=1)
        self.assertEqual(len(jobs), 2)

        # test list filter_by
        jobs = JobModel.list(filter_by={'id': 1})
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].dict(), test_job_dict)

    def test_update(self):
        init_job_data_dict = JobModel.get_by_pk(pk=1).dict()
        to_update_data_dict = dict(title=u'后端吃饭工程师',
                                   work_year=1,
                                   city_id=1,
                                   company_id=1,
                                   department='飞天面条神教招聘',
                                   salary='20k-32k',
                                   education=2,
                                   description=u'日常工作:吃饭！')

        affect_rows = JobModel.update(filter_by={'id': 1}, values=to_update_data_dict)
        self.assertEqual(affect_rows, 1)

        # 更新后预期的结果
        init_job_data_dict.update(**to_update_data_dict)
        predictive_job_data_dict = init_job_data_dict
        init_updated_at = init_job_data_dict.pop('updated_at')

        new_job_data_dict = JobModel.get_by_pk(pk=1).dict()
        self.assertDictContainsSubset(predictive_job_data_dict, new_job_data_dict)
        self.assertGreater(new_job_data_dict.updated_at, init_updated_at)

        # 其他记录不受影响
        self.assertEqual(JobModel.get_by_pk(pk=2).title, u'前端开发工程师')

        # 批量更改
        affect_rows = JobModel.update(filter_by={'city_id': 4}, values={'title': '测试'})
        self.assertEqual(affect_rows, 2)
        jobs = JobModel.list(filter_by={'city_id': 4})
        self.assertTrue(all([job.title == u'测试' for job in jobs]))

    def test_update_by_pk(self):
        affect_rows = JobModel.update_by_pk(pk=1, values={'title': '你好啊啊'})
        self.assertEqual(affect_rows, 1)
        self.assertEqual(JobModel.get_by_pk(pk=1).title, u'你好啊啊')

    def test_execute_sql_string(self):
        job_rows = JobModel.execute_sql_string(
            'SELECT id, title FROM job WHERE id = :id', {'id': 1})
        self.assertEqual(len(job_rows), 1)
        self.assertEqual(job_rows[0][0], 1)
        self.assertEqual(job_rows[0][1], u'高级前端开发工程师')

        job_rows = JobModel.execute_sql_string('SELECT id, title FROM job')
        self.assertEqual(len(job_rows), 3)
        self.assertEqual(job_rows[0][0], 1)
        self.assertEqual(job_rows[0][1], u'高级前端开发工程师')

        affect_rows = JobModel.execute_sql_string(
            "UPDATE job SET title = '测试' WHERE id = :id", {'id': 1})
        self.assertEqual(affect_rows, 1)
        job = JobModel.get_by_pk(pk=1)
        self.assertEqual(job.title, u'测试')

    def test_batch_add(self):
        # 插入了其他的类实例
        init_jobs_count = JobModel.count()
        model_instances = [CityModel(name='你好'),
                           JobModel(title='招聘资深前端工程师', city_id=1, company_id=2, lg_job_id=100056),
                           JobModel(title='招聘资深中端工程师', city_id=1, company_id=2, lg_job_id=100055), ]

        with self.assertRaises(ValueError):
            JobModel.batch_add(model_instances)

        self.assertEqual(JobModel.count(), init_jobs_count)

        model_instances = [JobModel(title='招聘资深前端工程师', city_id=1, company_id=2, lg_job_id=100056),
                           JobModel(title='招聘资深中端工程师', city_id=1, company_id=2, lg_job_id=100055), ]

        JobModel.batch_add(model_instances)

        self.assertEqual(JobModel.count(), init_jobs_count + 2)
