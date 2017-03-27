# coding=utf-8
from tests import BaseTestCase
from app.model.city import CityModel


class CityModelTestCase(BaseTestCase):
    def test_get_city(self):
        city = CityModel.get(id=2)
        self.assertEqual(city.id, 2)
        self.assertEqual(city.name, '北京')

        city = CityModel.get(name='北京')
        self.assertEqual(city.id, 2)
        self.assertEqual(city.name, '北京')

    def test_add_city(self):
        data = {
            'id': 1,
            'name': '测试1'
        }
        CityModel.add(**data)
        citys = CityModel.list()
        self.assertEqual(len(citys), 3)
        city = CityModel.get(id=1)
        for (key, value) in data.items():
            self.assertEqual(getattr(city, key), value)

    def test_list_city(self):
        citys = CityModel.list()
        self.assertEqual(len(citys), 2)
        self.assertEqual(citys[0].id, 2)
        self.assertEqual(citys[1].id, 3)
