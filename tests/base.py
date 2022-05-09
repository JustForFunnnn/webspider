#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from unittest import TestCase

from webspider.utils.sql import get_session
from tests.util import create_test_db, drop_test_db

here_dir = os.path.dirname(__file__)


class BaseTestCase(TestCase):
    session = get_session()

    def setUp(self):
        create_test_db(session=self.session)

    def tearDown(self):
        # 测试结束 销毁测试数据库
        drop_test_db(session=self.session)
