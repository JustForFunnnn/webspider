# coding=utf-8
from kombu import Queue
from kombu import Exchange
from celery.schedules import crontab

BROKER_URL = 'redis://127.0.0.1:6379'  # 指定 Broker

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # 指定 Backend

CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，默认是 UTC

CELERY_ENABLE_UTC = True

CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化 eg: json yaml msgpack pickle(不推荐)

CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 4  # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显

CELERY_IMPORTS = (  # 指定导入的任务模块
    'app.tasks.lagou_data.py'
)

CELERY_TASK_PUBLISH_RETRY = False  # 重试

# schedules
CELERYBEAT_SCHEDULE = {
    'crawl-jobs-count-task': {
        'task': 'app.tasks.job_quantity.crawl_lagou_job_quantity',
        'schedule': crontab(hour='00', minute='00', day_of_week='2, 5'),
    },
    'crawl_lagou_data-task': {
        'task': 'app.tasks.crawl_lagou_data',
        'schedule': crontab(hour='16', minute='10', day_of_month='5'),
    }
}

CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('lagou_data', Exchange('lagou_data'), routing_key='lagou_data'),
    # Queue('job_count', Exchange('job_count'), routing_key='job_count'),
)

CELERY_ROUTES = {
    # 'app.tasks.lagou_data.crawl_lagou_job_count': {'queue': 'job_quantity', 'routing_key': 'job_quantity'},
    'app.tasks.lagou_data.crawl_lagou_data_task': {'queue': 'lagou_data', 'routing_key': 'lagou_data'}
}
