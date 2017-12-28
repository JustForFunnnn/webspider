# # coding=utf-8
# from tests import BaseTestCase
# from webspider.controllers.city import CityController
#
#
# class CityControllerTestCase(BaseTestCase):
#     def test_get_city(self):
#         city_id = CityController.get_city_id_by_name(name='测试2')
#         self.assertEqual(city_id, 2)
#
#     def test_add_city(self):
#         data = {
#             'id': 1,
#             'name': '测试1'
#         }
#         CityController.add(**data)
#         citys = CityController.list()
#         self.assertEqual(len(citys), 3)
#         city_id = CityController.get_city_id_by_name(name='测试1')
#         for (key, value) in data.items():
#             self.assertEqual(getattr(city, key), value)
#
#     def test_list_city(self):
#         citys = CityModel.list()
#         self.assertEqual(len(citys), 2)
#         self.assertEqual(citys[0].id, 2)
#         self.assertEqual(citys[1].id, 3)
