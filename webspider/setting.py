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
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '3306')

# MYSQL 配置
MYSQL_CONF = {
    'host': 'mysql+mysqldb://{username}:{password}@{db_host}:{db_port}/spider?charset=utf8mb4'.format(
        username=MYSQL_USERNAME,
        password=MYSQL_PASSWORD,
        db_host=DB_HOST,
        db_port=DB_PORT
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
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'app': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'tornado': {
            'handlers': ['console', ],
            'level': 'DEBUG',
            'propagate': False,
        },
        'tornado.access': {
            'handlers': ['console', ],
            'propagate': False,
            'level': 'INFO',
        },
        'tornado.application': {
            'handlers': ['console', ],
            'propagate': False,
            'level': 'INFO',
        },
        'tornado.general': {
            'handlers': ['console', ],
            'propagate': False,
            'level': 'INFO',
        },
        'sqlalchemy.engine': {
            'handlers': ['console', ],
            'propagate': False,
            'level': 'INFO',
        },
        'gunicorn': {
            'level': 'INFO',
            'handlers': ['console', ],
            'propagate': False,
        },
    },
}
