# coding=utf-8
import logging.config

from common import config


__version__ = '0.0.2'

logging.config.dictConfig(config.LOGGING_CONFIG)
