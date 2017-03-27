# -*- coding: utf-8 -*-
from app.model.job import JobModel


class JobController(object):
    @classmethod
    def add(cls, id, company_id, city_id, title, work_year='', department='', salary='', education='', description='',
            advantage='', job_nature='', created_at=0):
        JobModel.add(id=id, title=title, city_id=city_id, company_id=company_id, work_year=work_year,
                     department=department, salary=salary, education=education, description=description,
                     advantage=advantage, job_nature=job_nature, created_at=created_at)

    @classmethod
    def count(cls, id=None, keyword_id=None):
        return JobModel.count(id=id, keyword_id=keyword_id)

    @classmethod
    def list(cls, keyword_id=None, limit=None, offset=None):
        return JobModel.list(keyword_id=keyword_id, limit=limit, offset=offset)



