# coding=utf-8
from kombu import Queue
from kombu import Exchange

from celery.schedules import crontab

BROKER_URL = 'redis://127.0.0.1:6379'  # 指定 Broker

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # 指定 Backend

CELERY_CREATE_MISSING_QUEUES = True  # 某个程序中出现的队列，在broker中不存在，则立刻创建它

CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，默认是 UTC

CELERYD_CONCURRENCY = 2  # 并发worker数

CELERY_ENABLE_UTC = False

CELERYD_FORCE_EXECV = True  # 强制退出

CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化

CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_IGNORE_RESULT = True  # 忽略任务结果

# CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 1  # 任务结果过期时间

CELERY_IMPORTS = (  # 指定导入的任务模块
    'webspider.tasks.actor.lagou_data',
    'webspider.tasks.actor.lagou_jobs_count',
    'webspider.tasks.actor.keyword_statistic',
)

CELERY_TASK_PUBLISH_RETRY = False  # 重试

CELERYBEAT_SCHEDULE = {
    'crawl_lagou_jobs_count_task': {
        'task': 'webspider.tasks.actor.lagou_jobs_count.crawl_lagou_jobs_count_task',
        'schedule': crontab(hour='01', minute='01', day_of_week='2, 5'),
    },
    'crawl_lagou_data_task': {
        'task': 'webspider.tasks.actor.lagou_data.crawl_lagou_data_task',
        'schedule': crontab(hour='01', minute='01', day_of_month='1'),
    },
    'update_keyword_statistic': {
        'task': 'webspider.tasks.actor.keyword_statistic.update_keywords_statistic_task',
        'schedule': crontab(hour='01', minute='01', day_of_week='1, 4'),
    },
}

default_exchange = Exchange('default', type='direct')
lagou_exchange = Exchange('lagou', type='direct')

CELERY_QUEUES = (
    Queue(name='default', exchange=default_exchange, routing_key='default'),
    Queue(name='lagou_data', exchange=lagou_exchange, routing_key='for_lagou_data'),
    Queue(name='lagou_jobs_data', exchange=lagou_exchange, routing_key='for_lagou_jobs_data'),
    Queue(name='lagou_jobs_count', exchange=lagou_exchange, routing_key='for_lagou_jobs_count'),
)

CELERY_ROUTES = {
    'webspider.tasks.actor.lagou_data.crawl_lagou_job_data_task': {'exchange': 'lagou',
                                                                   'routing_key': 'for_lagou_jobs_data'},
    'webspider.tasks.actor.lagou_jobs_count.*': {'exchange': 'lagou', 'routing_key': 'for_lagou_jobs_count'},
    'webspider.tasks.actor.lagou_data.*': {'exchange': 'lagou', 'routing_key': 'for_lagou_data'},
    '*': {'exchange': 'default', 'routing_key': 'default'}
}
