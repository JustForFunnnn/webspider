#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup

from webspider import __version__

# get the dependencies and installs
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'requirements.txt')) as f:
    all_requirements = f.read().split('\n')

setup(
    name='webspider',
    version=__version__,
    license='MIT',
    author='JustForFunnn',
    author_email='',
    description='web spider',
    url='https://github.com/JustForFunnnn/webspider',
    packages=find_packages(exclude=['tests']),
    package_data={'webspider': ['README.md']},
    zip_safe=False,
    install_requires=all_requirements,
    entry_points={
        'console_scripts': [
            'web = webspider.web.app:main',
            'production_web = webspider.quickly_cmd:run_web_app_by_gunicorn',
            'crawl_lg_data = webspider.tasks.actor.lg_data:crawl_lg_data_task',
            'crawl_lg_jobs_count = webspider.tasks.actor.lg_jobs_count:crawl_lg_jobs_count_task',
            # beat
            'celery_beat = webspider.quickly_cmd:run_celery_beat',
            'celery_flower = webspider.quickly_cmd.py:run_celery_flower',
            # worker
            'celery_default_worker = webspider.quickly_cmd:run_celery_default_worker',
            'celery_lg_data_worker = webspider.quickly_cmd:run_celery_lg_data_worker',
            'celery_lg_jobs_data_worker = webspider.quickly_cmd:run_celery_lg_jobs_data_worker',
            'celery_lg_jobs_count_worker = webspider.quickly_cmd:run_celery_lg_jobs_count_worker',
        ],
    }
)
