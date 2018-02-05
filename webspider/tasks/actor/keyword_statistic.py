# coding=utf-8
import logging
import json

from webspider.tasks.celery_app import celery_app
from webspider.controllers import keyword_statistic_ctl
from webspider.models import (KeywordModel, JobModel, JobKeywordModel, KeywordStatisticModel)

logger = logging.getLogger(__name__)


@celery_app.task()
def update_keywords_statistic_task():
    """更新关键词统计任务"""
    keywords = KeywordModel.list()
    for keyword in keywords:
        update_single_keyword_statistic_task.delay(keyword.id)


@celery_app.task()
def update_single_keyword_statistic_task(keyword_id):
    """更新关键词统计任务"""

    job_keywords = JobKeywordModel.list(filter_by={'keyword_id': keyword_id})
    jobs = JobModel.list(filter=(JobModel.id.in_([job_keyword.job_id for job_keyword in job_keywords])))
    if not jobs:
        return

    educations_statistic = keyword_statistic_ctl.get_educations_statistic(jobs=jobs)
    finance_stage_statistic = keyword_statistic_ctl.get_finance_stage_statistic(jobs=jobs)
    city_jobs_count_statistic = keyword_statistic_ctl.get_city_jobs_count_statistic(jobs=jobs)
    salary_statistic = keyword_statistic_ctl.get_salary_statistic(jobs=jobs)
    work_years_statistic = keyword_statistic_ctl.get_work_years_statistic(jobs=jobs)

    statistic_values = dict(
        keyword_id=keyword_id,
        educations=json.dumps(educations_statistic),
        city_jobs_count=json.dumps(city_jobs_count_statistic),
        salary=json.dumps(salary_statistic),
        financing_stage=json.dumps(finance_stage_statistic),
        work_years=json.dumps(work_years_statistic)
    )

    if KeywordStatisticModel.is_exist(filter_by={'keyword_id': keyword_id}):
        KeywordStatisticModel.update(filter_by={'keyword_id': keyword_id}, values=statistic_values)
    else:
        KeywordStatisticModel.add(**statistic_values)
