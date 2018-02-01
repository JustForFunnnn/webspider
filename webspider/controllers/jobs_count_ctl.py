# -*- coding: utf-8 -*-

from webspider.models import JobsCountModel
from webspider.utils.time_tools import datetime_to_timestamp


def get_per_day_jobs_count(keyword_id):
    all_jobs_count = JobsCountModel.list(filter_by={'keyword_id': keyword_id}, order_by=JobsCountModel.date.asc())
    all_jobs_count = [jobs_count.dict() for jobs_count in all_jobs_count]
    for jobs_count in all_jobs_count:
        jobs_count.created_at = datetime_to_timestamp(jobs_count.created_at)
        jobs_count.updated_at = datetime_to_timestamp(jobs_count.updated_at)
    return all_jobs_count
