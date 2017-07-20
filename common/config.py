# coding=utf-8
import os

# 如需要把错误日志发送到邮箱内 需配置以下环境变量
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
MAIL_USER_NAME = os.environ.get('MAIL_USER_NAME')
MAIL_USER_PASSWORD = os.environ.get('MAIL_USER_PASSWORD')
FROM_EMAIL_ADDRESS = os.environ.get('FROM_EMAIL_ADDRESS')
TO_EMAIL_ADDRESS = os.environ.get('TO_EMAIL_ADDRESS')
MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')

# MYSQL 配置
DB_CONF = {
    'host': 'mysql+mysqldb://{username}:{password}@localhost:3306/spider?charset=utf8mb4'.format(
        username=MYSQL_USERNAME,
        password=MYSQL_PASSWORD
    )
}

REDIS_CONF = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}

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
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'WARNING',
            'formatter': 'default',
            'class': 'logging.FileHandler',
            'filename': 'spider_log.txt',
            'encoding': 'utf8'
        },
        'smtp': {
            'level': 'ERROR',
            'class': 'logging.handlers.SMTPHandler',
            'formatter': 'default',
            'mailhost': (SMTP_HOST, SMTP_PORT),
            'fromaddr': FROM_EMAIL_ADDRESS,
            'toaddrs': [TO_EMAIL_ADDRESS],
            'subject': '爬虫系统出现异常',
            'credentials': (MAIL_USER_NAME, MAIL_USER_PASSWORD)
        }
    },

    'loggers': {
        '': {
            'handlers': ['console', 'file', 'smtp'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'app': {
            'handlers': ['console', 'file', 'smtp'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'tornado': {
            'handlers': ['console', 'file', 'smtp'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
