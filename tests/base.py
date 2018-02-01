#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from unittest import TestCase

from webspider.utils.sql import get_session
from tests.util import execute_sql_file, get_current_database_name

here_dir = os.path.dirname(__file__)


class BaseTestCase(TestCase):
    session = get_session()

    def setUp(self):
        test_db_name = 'test_spider'
        # 清除测试数据库
        self.session.execute("DROP DATABASE IF EXISTS {db_name};".format(db_name=test_db_name))
        # 创建测试数据库
        self.session.execute("CREATE DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;".format(
            db_name=test_db_name))
        # 指定测试数据库 test_spider
        self.session.execute("USE {db_name};".format(db_name=test_db_name))

        path = os.path.dirname(__file__)
        # 创建表
        execute_sql_file(
            file_paths=[os.path.join(path, "schema.sql"), ],
            db_session=self.session,
            expectant_db_name=test_db_name
        )
        fixture_path = os.path.join(path, 'fixture')
        # 装载表数据
        fixture_file_paths = [os.path.join(fixture_path, file) for file in os.listdir(fixture_path)]
        execute_sql_file(
            file_paths=fixture_file_paths,
            db_session=self.session,
            expectant_db_name=test_db_name
        )
        assert get_current_database_name(self.session) == 'test_spider'

    def teardown(self):
        # 测试结束 销毁测试数据库
        self.session.execute('DROP DATABASE test_spider;')
