# -*- coding: utf-8 -*-
from tornado.web import URLSpec

from webspider.web.handlers import StatisticsHandler, IndexHandler

url_handlers = [
    URLSpec(r"/", IndexHandler),
    URLSpec(r"/statistics", StatisticsHandler),
]
