# -*- coding: utf-8 -*-
from tornado.web import URLSpec

from app.web.handlers.keyword import KeywordHandler

url_handlers = [
    URLSpec(r"/keyword", KeywordHandler, name="keyword"),
    URLSpec(r"/", KeywordHandler, name="keyword"),
]
