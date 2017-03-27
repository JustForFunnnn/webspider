# coding=utf-8


BROKER_URL = 'redis://127.0.0.1:6379'  # 指定 Broker

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'  # 指定 Backend

CELERY_TIMEZONE = 'Asia/Shanghai'  # 指定时区，默认是 UTC

CELERY_ENABLE_UTC = True

CELERY_TASK_SERIALIZER = 'json'  # 任务序列化和反序列化 ls: json yaml msgpack pickle(不推荐)

CELERY_RESULT_SERIALIZER = 'json'  # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON

CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 4  # 任务过期时间，不建议直接写86400，应该让这样的magic数字表述更明显

CELERY_IMPORTS = (  # 指定导入的任务模块
    'app.tasks.job',
    'app.tasks.company'
)

CELERY_TASK_PUBLISH_RETRY = False  # 重试

# CELERY_TASK_PUBLISH_RETRY_POLICY = {
#     'max_retries': 3,
#     'interval_start': 10,
#     'interval_step': 5,
#     'interval_max': 20
# }

# from datetime import timedelta
# from celery.schedules import crontab
# schedules
# CELERYBEAT_SCHEDULE = {
#     'add-every-30-seconds': {
#          'task': 'celery_app.task1.add',
#          'schedule': timedelta(seconds=30),       # 每 30 秒执行一次
#          'args': (5, 8)                           # 任务函数参数
#     },
#     'multiply-at-some-time': {
#         'task': 'celery_app.task2.multiply',
#         'schedule': crontab(hour=9, minute=50),   # 每天早上 9 点 50 分执行一次
#         'args': (3, 7)                            # 任务函数参数
#     }
# }

# from kombu import Queue
#
# CELERY_QUEUES = ( # 定义任务队列
#
# Queue('default', routing_key='task.#'), # 路由键以“task.”开头的消息都进default队列
#
# Queue('web_tasks', routing_key='web.#'), # 路由键以“web.”开头的消息都进web_tasks队列
#
# )
#
# CELERY_DEFAULT_EXCHANGE = 'tasks' # 默认的交换机名字为tasks
#
# CELERY_DEFAULT_EXCHANGE_TYPE = 'topic' # 默认的交换类型是topic
#
# CELERY_DEFAULT_ROUTING_KEY = 'task.default' # 默认的路由键是task.default，这个路由键符合上面的default队列
#
# CELERY_ROUTES = {
#
#     'projq.tasks.add': { # tasks.add的消息会进入web_tasks队列
#
#     'queue': 'web_tasks',
#
#     'routing_key': 'web.add',
#
#     }
#
# }
# celery -A projq worker -Q web_tasks -l info 启动指定队列的worker
