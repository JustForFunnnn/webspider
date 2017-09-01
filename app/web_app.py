# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging
import logging.config

import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import options
from tornado.wsgi import WSGIAdapter

from common import config
from common import constants
from app.web.urls import url_handlers
from app.web.handlers.base import BaseHandler
from app.utils.cmd import parse_cmd

logger = logging.getLogger(__name__)


def make_wsgi_app():
    return tornado.wsgi.WSGIAdapter(make_app())


def make_app():
    logging.config.dictConfig(config.LOGGING_CONFIG)

    settings = {
        'debug': constants.DEBUG,
        'template_path': os.path.join(
            os.path.dirname(__file__), "web", "templates"
        ),
        'static_path': os.path.join(
            os.path.dirname(__file__), 'web', 'static'
        ),
        'default_handler_class ': BaseHandler
    }

    app = tornado.web.Application(url_handlers, **settings)
    return app


def main():
    parse_cmd()
    logger.info('================ spider web server has started ================ ')
    logger.info('       server start at port -> {}, debug mode = {}'.format(options.web_port, constants.DEBUG))
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.web_port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
