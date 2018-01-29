# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging.config

import tornado
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import options, define, parse_command_line
from tornado.wsgi import WSGIAdapter

from webspider import constants
from webspider.web.urls import url_handlers
from webspider.utils.log import config_logging

config_logging()
logger = logging.getLogger(__name__)


def make_wsgi_app():
    web_app = make_web_app()
    return tornado.wsgi.WSGIAdapter(web_app)


def make_web_app():
    settings = {
        'debug': constants.DEBUG,
        'template_path': os.path.join(
            os.path.dirname(__file__), "templates"
        ),
        'static_path': os.path.join(
            os.path.dirname(__file__), 'static'
        )
    }

    app = tornado.web.Application(url_handlers, **settings)
    return app


def main():
    define(name='port', default=8000, type=int, help='run on the given port')
    parse_command_line()
    logger.info('====== web server starting at http://0.0.0.0:{} ======'.format(options.port))
    if constants.DEBUG:
        logger.info('debug mode is enabled!!!')

    app = make_web_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    http_server.start()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
