# -*- coding: utf-8 -*-
from tornado.web import URLSpec

from app.web.handlers.index import IndexHandler, TestHandler
from app.web.handlers.keyword import KeywordHandler

url_handlers = [
    URLSpec(r"/", IndexHandler, name="index"),
    URLSpec(r"/keyword", KeywordHandler, name="keyword"),
    URLSpec(r"/test", TestHandler, name="test")
]
