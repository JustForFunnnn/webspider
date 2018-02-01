# -*- coding: utf-8 -*-
import json

from webspider import utils
from webspider.web.formatter.base import Field, Downgrade


class KeywordStatisticFormatter(object):
    FIELDS = [
        Field('educations', converter=json.loads, downgrade=Downgrade({})),
        Field('city_jobs_count', converter=json.loads, downgrade=Downgrade({})),
        Field('salary', converter=json.loads, downgrade=Downgrade({})),
        Field('financing_stage', converter=json.loads, downgrade=Downgrade({})),
        Field('work_years', converter=json.loads, downgrade=Downgrade({})),
        Field('per_day_jobs_count'),
        Field('created_at', converter=utils.time_tools.datetime_to_timestamp),
        Field('updated_at', converter=utils.time_tools.datetime_to_timestamp),
    ]
