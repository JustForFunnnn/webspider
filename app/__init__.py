# coding=utf-8
import os
import logging.config
from tornado.options import options

from common import config
from app.utils.cmd import parse_cmd

__version__ = '0.0.1'

logging.config.dictConfig(config.LOGGING_CONFIG)


def run_celery_jobs_count_worker():
    parse_cmd()
    logging.warning(options.celery_log_level)
    celery_log_level = options.celery_log_level
    celery_app_path = options.celery_app
    worker_numbers = options.worker_numbers
    os.system(
        u'bin/celery worker -A {celery_app_path} -n jobs_count_worker --loglevel={log_level} -Q jobs_count --concurrency={worker_numbers}'.format(
            celery_app_path=celery_app_path,
            log_level=celery_log_level,
            worker_numbers=worker_numbers))


def run_celery_lagou_data_worker():
    parse_cmd()
    logging.warning(options.celery_log_level)
    celery_log_level = options.celery_log_level
    celery_app_path = options.celery_app
    worker_numbers = options.worker_numbers
    os.system(
        u'bin/celery worker -A {celery_app_path} -n lagou_data_worker --loglevel={log_level} -Q lagou_data --concurrency={worker_numbers}'.format(
            celery_app_path=celery_app_path,
            log_level=celery_log_level,
            worker_numbers=worker_numbers))


def run_celery_beat():
    parse_cmd()
    celery_log_level = options.celery_log_level
    celery_app_path = options.celery_app
    os.system(u'bin/celery -A {celery_app_path} beat --loglevel={log_level}'.format(celery_app_path=celery_app_path,
                                                                                    log_level=celery_log_level))


def run_celery_flower():
    os.system(u'bin/celery flower --broker=redis://localhost:6379/0 --broker_api=redis://localhost:6379/0')
