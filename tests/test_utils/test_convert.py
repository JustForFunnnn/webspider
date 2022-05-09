# coding=utf-8
from unittest import TestCase

from webspider.constants import WORK_YEARS_REQUEST_DICT, JOB_NATURE_DICT, COMPANY_SIZE_DICT
from webspider.utils.convert import convert_dict_field_to_constants, convert_field_to_constants


class TestUtilConvert(TestCase):
    def test_convert_dict_field_to_constants(self):
        init_dict = {
            'work_year': '应届毕业生',
            'size': '没有人',
            'nature': '全职',
            'name': '沙师弟',
            'id': 3,
            'value': None
        }
        convert_dict_field_to_constants(init_dict)
        self.assertDictEqual(init_dict, {
            'work_year': WORK_YEARS_REQUEST_DICT['应届毕业生'],
            'size': COMPANY_SIZE_DICT['unknown'],
            'nature': JOB_NATURE_DICT['全职'],
            'name': '沙师弟',
            'id': 3,
            'value': None
        })

    def test_convert_field_to_constants(self):
        constant_value = convert_field_to_constants(field_name='work_year', field_value='应届毕业生')
        self.assertEqual(constant_value, WORK_YEARS_REQUEST_DICT['应届毕业生'])

        constant_value = convert_field_to_constants(field_name='work_year', field_value='家里蹲')
        self.assertEqual(constant_value, WORK_YEARS_REQUEST_DICT['unknown'])

        with self.assertRaises(ValueError):
            convert_field_to_constants(field_name='dinner', field_value='牛肉饭')
