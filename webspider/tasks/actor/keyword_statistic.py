# coding=utf-8
import logging

from webspider import utils
from webspider import crawlers
from webspider import constants
from webspider.tasks.celery_app import celery_app
from webspider.controllers import industry_ctl, keyword_ctl, city_ctl
from webspider.models import (KeywordModel, )

logger = logging.getLogger(__name__)


@celery_app.task()
def update_keywords_statistic_task():
    """更新关键词统计任务"""
    keywords = KeywordModel.list()
    for keyword in keywords:
        update_single_keyword_statistic_task(keyword.id)


def update_single_keyword_statistic_task(keywod_id):
    """更新关键词统计任务"""
    total_KeywordModel.count()
