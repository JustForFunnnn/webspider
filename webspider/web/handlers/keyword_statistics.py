# coding: utf-8
import json

from webspider.web.handlers.base import BasePageHandler, BaseApiHandler
from webspider.exceptions import ResourceNotFoundWebException
from webspider.models import KeywordModel, KeywordStatisticModel


class KeywordStatisticsApiHandler(BaseApiHandler):
    def get(self):
        keyword_name = self.get_argument('keyword_name', '')
        if not keyword_name:
            raise ResourceNotFoundWebException(u'请输入关键词')

        keyword = KeywordModel.get_one(filter_by={'name': keyword_name})
        if not keyword:
            raise ResourceNotFoundWebException(u'找不到该关键词')

        keyword_statistic = KeywordStatisticModel.get_one(filter_by={'keyword_id': keyword.id})
        if not keyword_statistic:
            raise ResourceNotFoundWebException(u'暂无该关键词的统计结果')

        self.auto_render(keyword_statistic)


class KeywordStatisticsPageHandler(BasePageHandler):
    def get(self):
        keyword_name = self.get_argument('keyword_name', '')
        if not keyword_name:
            raise ResourceNotFoundWebException(u'请输入关键词')

        keyword = KeywordModel.get_one(filter_by={'name': keyword_name})
        if not keyword:
            raise ResourceNotFoundWebException(u'找不到该关键词')

        keyword_statistic = KeywordStatisticModel.get_one(filter_by={'keyword_id': keyword.id})
        if not keyword_statistic:
            raise ResourceNotFoundWebException(u'暂无该关键词的统计结果')

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
