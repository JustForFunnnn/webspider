# coding: utf-8
from tornado.web import RequestHandler

from common import constants
from common.db import redis_instance
from webspider.controllers.keyword import KeywordController
from webspider.controllers.job import get_jobs_statistics
from webspider.web.handlers.base import BasePageHandler
from webspider.exceptions import ResourceNotFoundException


# TODO
class StatisticsHandler(BasePageHandler):
    def prepare(self):
        redis_instance.incr(constants.REDIS_VISITED_PEOPLES_COUNT_KEY)
        RequestHandler.prepare(self)

    def get(self):
        pass


class StatisticsPageHandler(BasePageHandler):
    def prepare(self):
        redis_instance.incr(constants.REDIS_VISITED_PEOPLES_COUNT_KEY)
        RequestHandler.prepare(self)

    def get(self):
        keyword_name = self.get_argument('keyword', 'python')
        keyword = KeywordController.get(name=keyword_name)
        if not keyword:
            raise ResourceNotFoundException()

        (keyword_job_quantity,
         educations_request_counter,
         finance_stage_distribution,
         city_job_quantityer,
         salary_distribution,
         work_years_request_analyze) = get_jobs_statistics(keyword.id)

        self.render("statistics.html",
                    keyword=keyword_name,
                    keyword_job_quantity=keyword_job_quantity,
                    educations_request_counter=educations_request_counter,
                    finance_stage_distribution=finance_stage_distribution,
                    city_job_quantityer=city_job_quantityer,
                    salary_distribution=salary_distribution,
                    work_years_request_analyze=work_years_request_analyze)
