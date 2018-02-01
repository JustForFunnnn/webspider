# -*- coding: utf-8 -*-
from tornado.web import URLSpec, RedirectHandler

from webspider.web.handlers import KeywordStatisticsApiHandler, KeywordStatisticsPageHandler

url_handlers = [
    URLSpec(r"/", RedirectHandler, {'url': '/statistics?keyword_name=python'}),
    URLSpec(r"/api/statistics", KeywordStatisticsApiHandler),
    URLSpec(r"/statistics", KeywordStatisticsPageHandler),
]
