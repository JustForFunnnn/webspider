# coding=utf-8
import logging
from datetime import datetime

from webspider import crawlers
from webspider.tasks.celery_app import celery_app
from webspider.controllers import keyword_ctl, job_keyword_ctl
from webspider.models import JobsCountModel

logger = logging.getLogger(__name__)


@celery_app.task()
def crawl_lagou_jobs_count_task():
    keyword_ids = job_keyword_ctl.get_most_frequently_keyword_ids(limit=1000)
    for keyword_id in keyword_ids:
        crawl_lagou_keyword_jobs_count_task.delay(keyword_id)


@celery_app.task()
def crawl_lagou_keyword_jobs_count_task(keyword_id):
    cities_name_map = {
        'all_city': u'全国',
        'beijing': u'北京',
        'shanghai': u'上海',
        'guangzhou': u'广州',
        'shenzhen': u'深圳',
        'hangzhou': u'杭州',
        'chengdu': u'成都',
    }
    keyword_name = keyword_ctl.get_keyword_name_by_id(keyword_id)
    jobs_count_dict = dict(keyword_id=keyword_id)
    for city_name_key, city_name in cities_name_map.items():
        jobs_count_dict[city_name_key] = crawlers.get_jobs_count_from_lagou(city_name=city_name,
                                                                            keyword_name=keyword_name)
    jobs_count_dict['date'] = int(datetime.today().strftime('%Y%m%d'))

    JobsCountModel.add(**jobs_count_dict)
