# coding=utf-8
from tests import BaseTestCase
from webspider.controllers import industry_ctl
from webspider.models import IndustryModel


class TestIndustryController(BaseTestCase):
    def test_get_industry_id_by_name(self):
        industry_id = industry_ctl.get_industry_id_by_name(name='开网吧')
        self.assertEqual(industry_id, 1000001)

        with self.assertRaises(ValueError):
            industry_ctl.get_industry_id_by_name(name='开飞机')

    def test_insert_industry_if_not_exist(self):
        industry_name = '开飞机'
        industry_id = industry_ctl.insert_industry_if_not_exist(industry_name)
        self.assertTrue(industry_id > 0)
        industry = IndustryModel.get_by_pk(pk=industry_id)
        self.assertEqual(industry.name, industry_name)

        self.assertIsNone(industry_ctl.insert_industry_if_not_exist(industry_name))
