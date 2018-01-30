# coding=utf-8
import logging

from webspider import utils
from webspider import crawlers
from webspider import constants
from webspider.tasks.celery_app import celery_app
from webspider.controllers import job_ctl, keyword_ctl
from webspider.models import (KeywordModel, KeywordStatisticModel, JobModel)

logger = logging.getLogger(__name__)


@celery_app.task()
def update_keywords_statistic_task():
    """更新关键词统计任务"""
    keywords = KeywordModel.list()
    for keyword in keywords:
        update_single_keyword_statistic_task(keyword.id)


def update_single_keyword_statistic_task(keyword_id):
    """更新关键词统计任务"""
    KeywordStatisticModel(keyword_id=keyword_id)


# def get_jobs_statistics(keyword_id):
#     keyword_job_quantity = job_ctl.list(keyword_id=keyword_id, sort_by='asc')
#     for item in keyword_job_quantity:
#         item.date_string = timestamp2string(timestamp=item.date, date_format='%m/%d')
#     jobs = keyword_ctl.list(filter_by={'keyword_id': keyword_id})
#     educations_request_counter = educations_request_analyze(jobs=jobs)
#     finance_stage_distribution = finance_stage_distribution_analyze(jobs=jobs)
#     city_job_quantityer = city_job_quantity_analyze(jobs=jobs)
#     salary_distribution = salary_distribution_analyze(jobs=jobs)
#     work_years_request = work_years_request_analyze(jobs=jobs)
#     return (keyword_job_quantity,
#             educations_request_counter,
#             finance_stage_distribution,
#             city_job_quantityer,
#             salary_distribution,
#             work_years_request)
