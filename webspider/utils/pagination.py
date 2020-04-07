# coding=utf-8
from math import ceil


class Pagination(object):
    """分页"""
    def __init__(self, page=1, per_page=10, total=0):
        self.page = page
        self.per_page = per_page
        self.total = total

    @property
    def pages(self):
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    @property
    def prev_num(self):
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_num(self):
        if not self.has_next:
            return None
        return self.page + 1

    @property
    def iter_pages(self):
        for num in range(1, self.pages + 1):
            yield num
