# coding=utf-8
from tests import BaseTestCase
from app.model.company import CompanyModel


class CompanyModelTestCase(BaseTestCase):
    def test_list_company(self):
        companys = CompanyModel.list()
        self.assertEqual(len(companys), 2)

    def test_add_company(self):
        data = {
            'id': 10001,
            'city_id': 2,
            'shortname': '短名',
            'fullname': '全名全名全名全名全名',
            'finance_stage': 3,
            'advantage': '优势和福利',
            'size': 3,
            'address': '北京市海淀区768创意园',
            'features': '公司一句话简介',
            'introduce': '公司长篇简介公司长篇简介公司长篇简介公司长篇简介公司长篇简介公司长篇简介',
            'process_rate': 95,
        }
        CompanyModel.add(**data)
        companys = CompanyModel.list()
        self.assertEqual(len(companys), 3)
        companys = CompanyModel.list(ids=[10001,])
        self.assertEqual(len(companys), 1)
        for (key, value) in data.items():
            self.assertEqual(getattr(companys[0], key), value)

    def test_count_company(self):
        count = CompanyModel.count()
        self.assertEqual(count, 2)

    def test_update_company(self):
        update_attr = {
            'shortname': '更新后的名称'
        }

        CompanyModel.update(10, update_attr)
        companys = CompanyModel.list(ids=[10, ])
        for (key, value) in update_attr.items():
            self.assertEqual(getattr(companys[0], key), value)
