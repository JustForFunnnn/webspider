# -*- coding: utf-8 -*-
from webspider import utils
from webspider.web.formatter.base import Field


class JobsCountFormatter(object):
    FIELDS = [
        Field('date'),
        Field('all_city'),
        Field('beijing'),
        Field('guangzhou'),
        Field('shenzhen'),
        Field('shanghai'),
        Field('hangzhou'),
        Field('chengdu'),
        Field('created_at', converter=utils.time_tools.datetime_to_timestamp),
        Field('updated_at', converter=utils.time_tools.datetime_to_timestamp),
    ]
