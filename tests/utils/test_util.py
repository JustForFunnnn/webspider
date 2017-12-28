# coding=utf-8
from unittest import TestCase

from webspider.utils.util import (update_salary_dict, get_salary_section, reverse_dict)


class UtilTestCase(TestCase):
    def test_update_salary(self):
        test_dict = {
            100: 1,
            101: 0,
            102: 0
        }
        update_salary_dict(test_dict, 100, 102)
        self.assertEqual(test_dict[100], 2)
        self.assertEqual(test_dict[101], 1)
        self.assertEqual(test_dict[102], 1)

        test_dict = update_salary_dict({}, 10, 30)
        for index in range(111):
            if 10 <= index <= 30:
                self.assertEqual(test_dict[index], 1)
            else:
                self.assertEqual(test_dict[index], 0)

    def test_get_salary_section(self):
        salary = '15k-25k'
        left, right = get_salary_section(salary)
        self.assertEqual(left, 15)
        self.assertEqual(right, 25)

        salary = '15k以上'
        left, right = get_salary_section(salary)
        self.assertEqual(left, 15)
        self.assertEqual(right, 20)

        salary = '15k以下'
        left, right = get_salary_section(salary)
        self.assertEqual(left, 10)
        self.assertEqual(right, 15)

    def test_reverse_dict(self):
        test_dict = {
            'one': 1,
            'two': 'three',
            3: 2,
            4: 'four',
        }
        new_dict = reverse_dict(old_dict=test_dict)
        self.assertEqual(new_dict[1], 'one')
        self.assertEqual(new_dict['three'], 'two')
        self.assertEqual(new_dict[2], 3)
        self.assertEqual(new_dict['four'], 4)
