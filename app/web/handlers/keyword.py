# coding: utf-8
from app.web.handlers.base import BaseHandler
from app.controllers.keyword import KeywordController
from app.controllers.jobs_count import JobsCountController
from app.controllers.job import JobController
from app.utils.time_tools import get_date_begin_by_timestamp, timestamp2string


class KeywordHandler(BaseHandler):
    def get(self):
        keyword_name = self.get_argument('keyword', 'python')
        keyword = KeywordController.get(name=keyword_name)
        if not keyword:
            self.write_error(404)
            return
        # 前2个月
        pre_two_month = get_date_begin_by_timestamp(after_days=-62)
        keyword_jobs_count = JobsCountController.list(keyword_id=keyword.id, start_time=pre_two_month, sort_by='asc')
        for item in keyword_jobs_count:
            item.date_string = timestamp2string(timestamp=item.date, date_format='%m/%d')
        jobs = JobController.list(keyword_id=keyword.id)
        educations_request_counter = JobController.educations_request_analyze(jobs=jobs)
        finance_stage_distribution = JobController.finance_stage_distribution_analyze(jobs=jobs)
        city_jobs_counter = JobController.city_jobs_count_analyze(jobs=jobs)
        salary_distribution = JobController.salary_distribution_analyze(jobs=jobs)
        work_years_request_analyze = JobController.work_years_request_analyze(jobs=jobs)
        self.render("keyword.html",
                    keyword=keyword_name,
                    keyword_jobs_count=keyword_jobs_count,
                    educations_request_counter=educations_request_counter,
                    finance_stage_distribution=finance_stage_distribution,
                    city_jobs_counter=city_jobs_counter,
                    salary_distribution=salary_distribution,
                    work_years_request_analyze=work_years_request_analyze)
