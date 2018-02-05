# coding=utf-8
from tests import BaseTestCase
from webspider.controllers import city_ctl
from webspider.models import CityModel


class TestCityController(BaseTestCase):
    def test_get_city_id_by_name(self):
        city_id = city_ctl.get_city_id_by_name(name='北京')
        self.assertEqual(city_id, 2)

        with self.assertRaises(ValueError):
            city_ctl.get_city_id_by_name(name='通利福尼亚')

    def test_insert_city_if_not_exist(self):
        city_id = city_ctl.insert_city_if_not_exist('湛江')
        self.assertTrue(city_id > 0)
        city = CityModel.get_by_pk(pk=city_id)
        self.assertEqual(city.name, '湛江')

        self.assertIsNone(city_ctl.insert_city_if_not_exist('湛江'))

    def test_get_city_name_dict(self):
        city_name_dict = city_ctl.get_city_name_dict()
        self.assertDictEqual(city_name_dict, {'北京': 2, '上海': 3, '广州': 4})
