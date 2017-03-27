# coding=utf-8
from tests import BaseTestCase
from app.model.industry import IndustryModel


class IndustryModelTestCase(BaseTestCase):
    def test_get_industry(self):
        industry = IndustryModel.get(name='移动互联网')
        self.assertEqual(industry.id, 24)
        self.assertEqual(industry.name, '移动互联网')

    def test_insert_if_not_exist_industry(self):
        data = {
            'name': '家里蹲',
        }
        IndustryModel.insert_if_not_exist(**data)
        industry = IndustryModel.get(name='家里蹲')
        self.assertEqual(industry.id, 10595)
        self.assertEqual(industry.name, '家里蹲')

        IndustryModel.insert_if_not_exist(**data)
        industry = IndustryModel.get(name='家里蹲')
        self.assertEqual(industry.id, 10595)
        self.assertEqual(industry.name, '家里蹲')
