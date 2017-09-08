# coding: utf-8
from common import constants
from common.db import redis_instance
from app.web.handlers.base import BaseHandler
from app.controllers.keyword import KeywordController
from app.controllers.job import JobController


class KeywordHandler(BaseHandler):
    def get(self):
        # 统计访问人数  incr() 操作线程安全
        redis_instance.incr(constants.REDIS_VISITED_PEOPLES_COUNT_KEY)
        keyword_name = self.get_argument('keyword', 'python')
        keyword = KeywordController.get(name=keyword_name)
        if not keyword:
            self.write_error(404)
            return

        (keyword_jobs_count,
         educations_request_counter,
         finance_stage_distribution,
         city_jobs_counter,
         salary_distribution,
         work_years_request_analyze) = JobController.get_jobs_statistics(keyword_id=keyword.id)

        self.render("keyword.html",
                    keyword=keyword_name,
                    keyword_jobs_count=keyword_jobs_count,
                    educations_request_counter=educations_request_counter,
                    finance_stage_distribution=finance_stage_distribution,
                    city_jobs_counter=city_jobs_counter,
                    salary_distribution=salary_distribution,
                    work_years_request_analyze=work_years_request_analyze)
