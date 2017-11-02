#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from setuptools import find_packages, setup

from app import __version__

# get the dependencies and installs
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'requirements.txt')) as f:
    all_requirements = f.read().split('\n')

setup(
    name='webspider',
    version=__version__,
    license='MIT',
    author='heguozhu',
    author_email='heguozhu@zhihu.com',
    description='lagou.com spider',
    url='git@github.com:GuozhuHe/webspider.git',
    packages=find_packages(exclude=['tests']),
    package_data={'webspider': ['README.md']},
    zip_safe=False,
    install_requires=all_requirements,
    entry_points={
        'console_scripts': [
            'web = app.web_app:main',
            'production_web = app.quickly_cmd:run_web_app_by_gunicorn',
            'crawl_lagou_data = app.tasks:crawl_lagou_data',
            'crawl_jobs_count = app.tasks.jobs_count:crawl_lagou_jobs_count',
            'celery_jobs_count_worker = app.quickly_cmd:run_celery_jobs_count_worker',
            'celery_lagou_data_worker = app.quickly_cmd:run_celery_lagou_data_worker',
            'celery_beat = app.quickly_cmd:run_celery_beat',
            'celery_flower = app.quickly_cmd.py:run_celery_flower',
        ],
    }
)
