# coding: utf-8
import os
import logging.config

from webspider import setting

LOG_FILE_PATH = os.path.join(setting.BASE_DIR, 'log', 'spider_log.txt')

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'default': {
            'format': '%(asctime)s- %(module)s:%(lineno)d [%(levelname)1.1s] %(name)s: %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S'
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'formatter': 'default',
            'class': 'logging.StreamHandler'
        },
        'smtp': {
            'level': 'ERROR',
            'class': 'logging.handlers.SMTPHandler',
            'formatter': 'default',
            'mailhost': (setting.SMTP_CONF['host'], setting.SMTP_CONF['port']),
            'fromaddr': setting.SMTP_CONF['from_email'],
            'toaddrs': [setting.SMTP_CONF['to_email'], ],
            'subject': '爬虫系统出现异常',
            'credentials': (setting.MAIL_CONF['username'], setting.MAIL_CONF['password'])
        },
        'file': {
            'level': 'ERROR',
            'formatter': 'default',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE_PATH,
            'encoding': 'utf8'
        },
    },

    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'webspider': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'tornado': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'tornado.access': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'tornado.application': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'tornado.general': {
            'handlers': ['console', 'file'],
            'propagate': False,
            'level': 'INFO',
        },
        'sqlalchemy.engine': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'gunicorn': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


def config_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
