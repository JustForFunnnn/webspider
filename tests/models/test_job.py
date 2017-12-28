# coding=utf-8
from sqlalchemy import and_, func

from tests import BaseTestCase
from webspider.model.job import JobModel

test_job_data = dict(id=4789,
                     title=u'Android开发工程师',
                     work_year=1,
                     city_id=3,
                     company_id=10,
                     department='堆糖技术部招聘',
                     salary='10k-20k',
                     education=3,
                     description=u'职位描述，福利等等 blablabla....',
                     advantage='发展空间大，成长快',
                     nature=0,
                     created_at=1494864000,
                     updated_at=1495006329)


class JobModelTestCase(BaseTestCase):
    def test_pk_name(self):
        self.assertEqual(JobModel.pk_name, 'id')

    def test_pk(self):
        self.assertEqual(JobModel.pk, JobModel.id)

    def test_get_by_pk(self):
        job = JobModel.get_by_pk(pk=4789)
        self.assertDictEqual(job.dict(), test_job_data)

    def test_model_to_dict(self):
        job = JobModel.get_by_pk(pk=4789).dict()
        self.assertTrue(isinstance(job, dict))
        self.assertDictEqual(job, test_job_data)

    def test_add(self):
        to_add_data_dict = dict(title=u'后端吃饭工程师',
                                work_year=2,
                                city_id=1,
                                company_id=1,
                                department='飞天面条神教招聘',
                                salary='20k-30k',
                                education=2,
                                description=u'日常工作:吃饭！',
                                advantage='饭管饱, 管够',
                                nature=0)
        job_id = JobModel.add(**to_add_data_dict)

        self.assertTrue(job_id > 0)
        job = JobModel.get_by_pk(pk=job_id)
        self.assertDictContainsSubset(to_add_data_dict, job.dict())
        self.assertGreater(job.created_at, 0)
        self.assertGreater(job.updated_at, 0)

    def test_get_one(self):
        # test get by filter
        job = JobModel.get_one(filter=(JobModel.id == 4789)).dict()
        self.assertDictEqual(job, test_job_data)

        job = JobModel.get_one(filter=and_(JobModel.id == 4789, JobModel.created_at > 0)).dict()
        self.assertDictEqual(job, test_job_data)

        # test get by filter
        job = JobModel.get_one(filter_by={'id': 4789}).dict()
        self.assertDictEqual(job, test_job_data)

        job = JobModel.get_one(filter_by={'id': 4789}, filter=(JobModel.work_year == 1)).dict()
        self.assertDictEqual(job, test_job_data)

    def test_list(self):
        # test list
        jobs = JobModel.list()
        self.assertEqual(len(jobs), 2)
        self.assertDictEqual(jobs[0].dict(), test_job_data)

        # test list limit
        jobs = JobModel.list(limit=1)
        self.assertEqual(len(jobs), 1)

        # test list offset
        jobs = JobModel.list(offset=1)
        self.assertEqual(len(jobs), 1)

        # test list filter_by
        jobs = JobModel.list(filter_by={'id': 4789})
        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0].dict(), test_job_data)

        jobs = JobModel.list(filter_by={'id': 1})
        self.assertEqual(len(jobs), 0)

        # test list order_by
        jobs = JobModel.list(order_by=JobModel.id.desc())
        self.assertEqual(jobs[1].dict(), test_job_data)

    def test_count(self):
        job_quantitys = JobModel.count()
        self.assertEqual(job_quantitys, 2)

        # test count filter_by
        job_quantitys = JobModel.count(filter_by={'id': 4789})
        self.assertEqual(job_quantitys, 1)

        job_quantitys = JobModel.count(filter_by={'id': 1})
        self.assertEqual(job_quantitys, 0)

    def test_update(self):
        init_job_data_dict = JobModel.get_by_pk(pk=4789).dict()
        to_update_data_dict = dict(title=u'后端吃饭工程师',
                                   work_year=2,
                                   city_id=1,
                                   company_id=11,
                                   department='飞天面条神教招聘',
                                   salary='20k-30k',
                                   education=2,
                                   description=u'日常工作:吃饭！')

        affect_rows = JobModel.update(filter_by={'id': 4789}, values=to_update_data_dict)
        self.assertEqual(affect_rows, 1)

        # 更新后预期的结果
        init_job_data_dict.update(**to_update_data_dict)
        expected_job_data_dict = init_job_data_dict
        init_updated_at = init_job_data_dict.pop('updated_at')

        new_job_data_dict = JobModel.get_by_pk(pk=4789).dict()
        self.assertDictContainsSubset(expected_job_data_dict, new_job_data_dict)
        self.assertGreater(new_job_data_dict.updated_at, init_updated_at)

        # 其他记录不受影响
        self.assertEqual(JobModel.get_by_pk(pk=6814).title, u'web前端')

        # 批量更改
        affect_rows = JobModel.update(filter_by={'company_id': 11}, values={'title': '测试'})
        self.assertEqual(affect_rows, 2)
        self.assertEqual(JobModel.get_by_pk(pk=6814).title, u'测试')
        self.assertEqual(JobModel.get_by_pk(pk=4789).title, u'测试')

    def test_update_by_pk(self):
        affect_rows = JobModel.update_by_pk(pk=6814, values={'title': '你好啊啊'})
        self.assertEqual(affect_rows, 1)
        self.assertEqual(JobModel.get_by_pk(pk=6814).title, u'你好啊啊')

    def test_execute_sql_string(self):
        job_rows = JobModel.execute_sql_string('select id, title from job where id = :id', {'id': 4789})
        self.assertEqual(len(job_rows), 1)
        self.assertEqual(job_rows[0][0], 4789)
        self.assertEqual(job_rows[0][1], u'Android开发工程师')

        job_rows = JobModel.execute_sql_string('select id, title from job')
        self.assertEqual(len(job_rows), 2)
        self.assertEqual(job_rows[0][0], 4789)
        self.assertEqual(job_rows[0][1], u'Android开发工程师')

        affect_rows = JobModel.execute_sql_string("update job set title = '测试' where id = :id", {'id': 4789})
        self.assertEqual(affect_rows, 1)
        job = JobModel.get_by_pk(pk=4789)
        self.assertEqual(job.title, u'测试')
