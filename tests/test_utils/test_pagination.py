# coding=utf-8
from unittest import TestCase

from webspider.utils.pagination import Pagination


class TestUtilPagination(TestCase):
    def test_pagination(self):
        pagination = Pagination(page=2, total=20, per_page=6)
        self.assertEqual(pagination.pages, 4)
        self.assertEqual(pagination.prev_num, 1)
        self.assertEqual(pagination.has_prev, True)
        self.assertEqual(pagination.next_num, 3)
        self.assertEqual(pagination.has_next, True)
        self.assertEqual([page for page in pagination.iter_pages], [1, 2, 3, 4])

    def test_pagination_no_pages(self):
        pagination = Pagination(page=2, total=20, per_page=0)
        self.assertEqual(pagination.pages, 0)

    def test_pagination_no_pre(self):
        pagination = Pagination(page=1, total=20, per_page=6)
        self.assertEqual(pagination.has_prev, False)
        self.assertEqual(pagination.prev_num, None)
        self.assertEqual(pagination.has_next, True)
        self.assertEqual(pagination.next_num, 2)

    def test_pagination_no_next(self):
        pagination = Pagination(page=4, total=20, per_page=6)
        self.assertEqual(pagination.has_prev, True)
        self.assertEqual(pagination.prev_num, 3)
        self.assertEqual(pagination.has_next, False)
        self.assertEqual(pagination.next_num, None)
