# -*- coding: utf-8 -*-
from app.model.jobs_count import JobsCountModel


class JobsCountController(object):
    @classmethod
    def add(cls, date, keyword_id, all_city, beijing, guangzhou, shenzhen, shanghai, hangzhou, chengdu):
        JobsCountModel.add(date=date, keyword_id=keyword_id, all_city=all_city, beijing=beijing, guangzhou=guangzhou,
                           shenzhen=shenzhen, shanghai=shanghai, hangzhou=hangzhou, chengdu=chengdu)

    @classmethod
    def list(cls, keyword_id=None, start_time=None, end_time=None, sort_by='desc'):
        return JobsCountModel.list(keyword_id=keyword_id, start_time=start_time, end_time=end_time, sort_by=sort_by)