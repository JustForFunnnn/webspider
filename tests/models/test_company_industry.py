# coding=utf-8
from tests import BaseTestCase
from app.model.company_industry import CompanyIndustryModel


class CompanyIndustryModelTestCase(BaseTestCase):
    def test_list_company_industry(self):
        company_industrys = CompanyIndustryModel.list()
        self.assertEqual(len(company_industrys), 2)

    def test_add_company_industry(self):
        data = {
            'company_id': 12,
            'city_id': 2,
            'industry_id': 25
        }
        CompanyIndustryModel.add(**data)
        company_industrys = CompanyIndustryModel.list()
        self.assertEqual(len(company_industrys), 3)
        company_industrys = CompanyIndustryModel.list(company_id=12)
        self.assertEqual(len(company_industrys), 1)
        for (key, value) in data.items():
            self.assertEqual(getattr(company_industrys[0], key), value)
