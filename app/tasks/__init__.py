# coding=utf-8
from celery import Celery

celery_app = Celery('tasks', include=['app.tasks.job', 'app.tasks.company', 'app.tasks.jobs_count'])
celery_app.config_from_object('app.tasks.celery_config')
