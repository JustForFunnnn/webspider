# coding: utf-8
import json

from webspider.web.handlers.base import BasePageHandler, BaseApiHandler
from webspider.exceptions import ResourceNotFoundException
from webspider.controllers import keyword_ctl, keyword_statistic_ctl


class KeywordStatisticsApiHandler(BaseApiHandler):
    def get(self):
        keyword_name = self.get_argument('keyword_name', '')
        if not keyword_name:
            raise ResourceNotFoundException(u'请输入关键词')

        keyword_id = keyword_ctl.get_keyword_id_by_name(name=keyword_name)
        if not keyword_id:
            raise ResourceNotFoundException(u'找不到该关键词')

        keyword_statistic = keyword_statistic_ctl.get_keyword_statistic(keyword_id=keyword_id)
        if not keyword_statistic:
            raise ResourceNotFoundException(u'暂无该关键词的统计结果')

        self.auto_render(keyword_statistic)


class KeywordStatisticsPageHandler(BasePageHandler):
    def get(self):
        keyword_name = self.get_argument('keyword_name', '')
        if not keyword_name:
            raise ResourceNotFoundException(u'请输入关键词')

        keyword_id = keyword_ctl.get_keyword_id_by_name(name=keyword_name)
        if not keyword_id:
            raise ResourceNotFoundException(u'找不到该关键词')

        keyword_statistic = keyword_statistic_ctl.get_keyword_statistic(keyword_id=keyword_id)
        if not keyword_statistic:
            raise ResourceNotFoundException(u'暂无该关键词的统计结果')

        self.render(
            "statistics.html",
            keyword_name=keyword_name,
            educations_statistic=json.loads(keyword_statistic.educations),
            city_jobs_count_statistic=json.loads(keyword_statistic.city_jobs_count),
            salary_statistic=json.loads(keyword_statistic.salary),
            finance_stage_statistic=json.loads(keyword_statistic.financing_stage),
            work_years_statistic=json.loads(keyword_statistic.work_years),
            per_day_jobs_count_statistic=keyword_statistic.per_day_jobs_count
        )
