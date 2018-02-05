# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from urllib.parse import urlencode

from tornado.testing import AsyncHTTPTestCase
from tornado.escape import json_encode, json_decode

from webspider.utils.sql import get_session
from webspider.web.app import make_web_app
from tests.util import create_test_db, drop_test_db

logger = logging.getLogger(__file__)


class BaseHandlerTestCase(AsyncHTTPTestCase):
    session = get_session()

    def setUp(self):
        create_test_db(self.session)
        super(BaseHandlerTestCase, self).setUp()

    def tearDown(self):
        drop_test_db(self.session)
        super(BaseHandlerTestCase, self).tearDown()

    def get_app(self):
        return make_web_app()

    def request(self, method, url, headers=None, data=None, json=None, form=None, **kwargs):
        if not headers:
            headers = {}

        if json is not None:
            headers['Content-Type'] = 'application/json'
            data = json_encode(json)

        elif form is not None:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            data = urlencode(form)

        response = self.fetch(url, method=method, headers=headers, body=data, allow_nonstandard_methods=True,
                              **kwargs)

        if response.code / 100 != 2:
            logger.error(response.body)

        return response

    def get(self, url, **kwargs):
        return self.request(url=url, method="GET", **kwargs)

    def post(self, url, **kwargs):
        return self.request(url=url, method="POST", **kwargs)

    def put(self, url, **kwargs):
        return self.request(url=url, method="PUT", **kwargs)

    def fetch_json(self, path, **kwargs):
        response = self.request('GET', path, **kwargs)
        if response.code / 100 != 2:
            raise ValueError('fetch json expect http code 2xx, got {}'.format(response.code))
        return json_decode(response.body)
