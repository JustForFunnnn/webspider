import os
import logging
from unittest import TestCase

from sqlalchemy.exc import OperationalError

from webspider.model.base import BaseModel
from webspider.utils.util import execute_sql_file


class BaseTestCase(TestCase):
    session = BaseModel.session

    def setUp(self):
        # 使用测试数据库
        try:
            self.session.execute("DROP DATABASE test_spider;")
        except OperationalError as e:
            logging.warning(e)
        self.session.execute("CREATE DATABASE test_spider CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        # 使用测试数据库 test_spider
        self.session.execute("USE test_spider;")
        path = os.path.dirname(__file__)
        execute_sql_file(
            file_paths=[os.path.join(path, "schema.sql"), ],
            db_session=self.session
        )
        fixture_path = os.path.join(path, 'fixture')
        # 装置 fixture 下的 SQL 记录......
        fixture_file_paths = [os.path.join(fixture_path, file) for file in os.listdir(fixture_path)]
        execute_sql_file(
            file_paths=fixture_file_paths,
            db_session=self.session
        )

    def teardown(self):
        # 测试结束 销毁测试数据库
        self.session.execute('DROP DATABASE test_spider;')
