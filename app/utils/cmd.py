# coding=utf-8

import tornado
from tornado.options import options, define

define(name='web_port', default=8000, type=int, help='run on the given port')
define(name="celery_log_level", default='debug', help=u"set the log level for celery", type=str)
define(name="celery_app", default='app.tasks.celery_app', help=u"celery app path", type=str)
define(name="worker_numbers", default=1, help=u"celery worker numbers", type=int)


def parse_cmd():
    tornado.options.parse_command_line()

