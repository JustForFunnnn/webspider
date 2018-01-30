# coding=utf-8
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# smtp
SMTP_HOST = os.environ.get('SMTP_HOST')
SMTP_PORT = os.environ.get('SMTP_PORT')
# email
MAIL_USER_NAME = os.environ.get('MAIL_USER_NAME')
MAIL_USER_PASSWORD = os.environ.get('MAIL_USER_PASSWORD')
FROM_EMAIL_ADDRESS = os.environ.get('FROM_EMAIL_ADDRESS')
TO_EMAIL_ADDRESS = os.environ.get('TO_EMAIL_ADDRESS')
# MYSQL
MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '3306')
# REDIS
REDIS_HOST = os.environ.get('DB_HOST', 'localhost')
REDIS_PORT = os.environ.get('DB_PORT', '6379')

# MYSQL 配置
MYSQL_CONF = {
    'connect_string': 'mysql+mysqldb://{username}:{password}@{db_host}:{db_port}/spider?charset=utf8mb4'.format(
        username=MYSQL_USERNAME,
        password=MYSQL_PASSWORD,
        db_host=DB_HOST,
        db_port=DB_PORT
    ),
    'host': DB_HOST,
    'port': DB_PORT,
    'username': MYSQL_USERNAME,
    'password': MYSQL_PASSWORD,
}

SMTP_CONF = {
    'host': SMTP_HOST,
    'port': SMTP_PORT,
    'from_email': FROM_EMAIL_ADDRESS,
    'to_email': TO_EMAIL_ADDRESS,
}

MAIL_CONF = {
    'username': MAIL_USER_NAME,
    'password': MAIL_USER_PASSWORD,
}

REDIS_CONF = {
    'host': REDIS_HOST,
    'port': REDIS_PORT
}
