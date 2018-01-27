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
            'web = webspider.web.app:main',
            'production_web = webspider.quickly_cmd:run_web_app_by_gunicorn',
            'crawl_lagou_data = webspider.tasks.actor.lagou_data:crawl_lagou_data_task',
            'celery_job_quantity_worker = webspider.quickly_cmd:run_celery_job_quantity_worker',
            'celery_lagou_data_worker = webspider.quickly_cmd:run_celery_lagou_data_worker',
            'celery_beat = webspider.quickly_cmd:run_celery_beat',
            'celery_flower = webspider.quickly_cmd.py:run_celery_flower',
        ],
    }
)
