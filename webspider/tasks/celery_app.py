# coding=utf-8

from celery import Celery

celery_app = Celery('tasks', include=['app.tasks.lagou_data'])
celery_app.config_from_object('app.tasks.celery_config')
