# -*- coding: utf-8 -*-
from app.model.job_keyword import JobKeywordModel


class JobKeywordController(object):
    @classmethod
    def add(cls, job_id, keyword_id, city_id):
        return JobKeywordModel.add(job_id=job_id, keyword_id=keyword_id, city_id=city_id)
