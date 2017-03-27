# coding=utf-8
from __future__ import absolute_import
import logging

from celery import Celery

celery_app = Celery('tasks', include=['app.tasks.job', 'app.tasks.company'])
celery_app.config_from_object('app.tasks.celery_config')

from common import constants
from common.db import redis_instance
from app.tasks.city import update_city_data
from app.tasks.company import update_company_data

logger = logging.getLogger(__name__)


def crawl_lagou_data(update_job=True, use_celery=False):
    """
    爬取拉勾上 company, city 的数据
    :param update_job: 是否更新工作的数据
    :param use_celery: 是否使用celery爬取
    :return:
    """
    update_city_data()
    logger.info('update_city_task 任务结束 !')
    # 北京:2 上海:3 深圳:215 广州:213 杭州:6 成都:252
    city_ids = [2, 3, 6, 79, 184, 213, 215, 298, 252]
    finance_stage_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    industry_ids = [0, 24, 25, 26, 27, 28, 29, 31, 32, 33, 34, 35, 38, 41, 43, 45, 47, 48, 49, 10594]
    # 用 redis 在不同的 worker 中共享数据， 首先清空相关 key
    redis_instance.delete(constants.REDIS_VISITED_COMPANY_KEY)

    for city_id in city_ids:
        for finance_stage_id in finance_stage_ids:
            for industry_id in industry_ids:
                if use_celery:
                    update_company_data.delay(city_id=city_id, finance_stage_id=finance_stage_id,
                                              industry_id=industry_id, update_job=update_job)
                else:
                    update_company_data(city_id=city_id, finance_stage_id=finance_stage_id, industry_id=industry_id,
                                        update_job=update_job)
    logger.info('任务结束 !')
