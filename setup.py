#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from app import __version__

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
    install_requires=[
        'requests',
        'sqlalchemy',
        'python-redis',
        'redis',
        'mysqlclient',
        'lxml',
        'retrying',
        'celery',
        'tornado',
    ],
    entry_points={
        'console_scripts': [
            'web = app.main:main',
            'spider = app.tasks:crawl_lagou_data'
        ],
    },
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
