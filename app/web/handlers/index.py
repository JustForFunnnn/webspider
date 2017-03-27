# coding: utf-8


from app.web.handlers.base import BaseHandler
from app.controllers.job import JobController
from app.controllers.company import CompanyController


class IndexHandler(BaseHandler):
    def get(self):
        company_count = CompanyController.count()
        job_count = JobController.count()
        last_updated_time = CompanyController.get_company_last_update_time()
        self.render("index.html", company_count=company_count, job_count=job_count, last_updated_time=last_updated_time)


class TestHandler(BaseHandler):
    def get(self):
        question_type = self.get_argument('question_type', None)
        is_org = self.get_argument('is_org', 0)
        if question_type is None:
            question_type = 1 if int(is_org) else 0
        self.write('question_type:{} , is_org:{}'.format(question_type,is_org))
