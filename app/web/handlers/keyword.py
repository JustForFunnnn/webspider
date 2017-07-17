# coding: utf-8
import logging

from app.web.handlers.base import BaseHandler
from app.controllers.keyword import KeywordController
from app.controllers.job import JobController


class KeywordHandler(BaseHandler):
    def get(self):
        keyword_name = self.get_argument('keyword', 'python')
        keyword = KeywordController.get(name=keyword_name)
        if not keyword:
            self.write_error(404)
            return
        jobs = JobController.list(keyword_id=keyword.id)
        educations_request_counter = JobController.educations_request_analyze(jobs=jobs)
        finance_stage_distribution = JobController.finance_stage_distribution_analyze(jobs=jobs)
        city_jobs_counter = JobController.city_jobs_count_analyze(jobs=jobs)
        salary_distribution = JobController.salary_distribution_analyze(jobs=jobs)
        work_years_request_analyze = JobController.work_years_request_analyze(jobs=jobs)
        self.render("keyword.html",
                    keyword=keyword_name,
                    educations_request_counter=educations_request_counter,
                    finance_stage_distribution=finance_stage_distribution,
                    city_jobs_counter=city_jobs_counter,
                    salary_distribution=salary_distribution,
                    work_years_request_analyze=work_years_request_analyze)
