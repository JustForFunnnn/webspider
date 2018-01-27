# coding=utf-8
# flake8: noqa
import os

"""
    拉勾工作类型
"""


class LagouJobType(object):
    all = '全部'
    technology = '技术'
    product = '产品'
    design = '设计'
    operation = '运营'
    sell_and_market = '市场与销售'
    function = '职能'


"""
    公司融资阶段
"""
FINANCE_STAGE_DICT = {
    'unknown': 0,
    '未融资': 1,
    '天使轮': 2,
    'A轮': 3,
    'B轮': 4,
    'C轮': 5,
    'D轮及以上': 6,
    '上市公司': 7,
    '不需要融资': 8,
}

"""
    工作性质
"""
JOB_NATURE_DICT = {
    'unknown': 0,
    '全职': 1,
    '兼职': 2,
    '实习': 3,
}

"""
     工作年限要求
"""
WORK_YEARS_REQUEST_DICT = {
    'unknown': 0,
    '不限': 1,
    '应届毕业生': 2,
    '1年以下': 3,
    '1-3年': 4,
    '3-5年': 5,
    '5-10年': 6,
    '10年以上': 7,
}

"""
     学历要求
"""
EDUCATION_REQUEST_DICT = {
    'unknown': 0,
    '不限': 1,
    '大专': 2,
    '本科': 3,
    '硕士': 4,
    '博士': 5,
}

"""
    公司规模
"""
COMPANY_SIZE_DICT = {
    'unknown': 0,
    '少于15人': 1,
    '15-50人': 2,
    '50-150人': 3,
    '150-500人': 4,
    '500-2000人': 5,
    '2000人以上': 6,
}

"""
    其他常量
"""

DEBUG = (os.environ.get('ENV', 'dev') == 'dev')

MIN_PROXY_COUNT = 30

HTTP_PROXY_FORMATTER = "http://{ip}:{port}"

HTTPS_PROXY_FORMATTER = "https://{ip}:{port}"

TIMEOUT = 4

# 爬虫最小睡眠时间
MIN_SLEEP_SECS = 3

# 爬虫最大睡眠时间
MAX_SLEEP_SECS = 5

REDIS_VISITED_PEOPLES_COUNT_KEY = 'visited_peoples_count'

"""
    字段长度限制
"""
COMPANY_INTRODUCE_MAX_LEN = 2048
COMPANY_ADVANTAGE_MAX_LEN = 256
JOB_DESCRIPTION_MAX_LEN = 2048
JOB_ADVANTAGE_MAX_LEN = 256

"""
    retry 相关
"""
# 用来设定最大的尝试次数，超过该次数就停止重试
RETRY_TIMES = 3
# 函数最久持续时间
STOP_MAX_DELAY = 1000 * 30
# 设置在两次retrying之间的停留时间
WAIT_FIXED = 1000 * 2

"""
    HTTP 相关 (基于减少 lagou 的网站负载考虑, 屏蔽以下常量的实际内容)
"""
HTTP_HEADER = {}

USER_AGENT_LIST = {}

"""
    拉勾相关网页 (基于减少 lagou 的网站负载考虑, 屏蔽以下常量的实际内容)
"""

JOB_JSON_URL = ''

JOB_DETAIL_URL = ''

COMPANY_DETAIL_URL = ''

ALL_CITY_URL = ''

COMPANIES_URL = ''

COMPANY_JOBS_URL = ''

# COMPANIES_URL sort field
SORTED_BY_JOBS_COUNT = 1

# 生产环境 和 个人开发环境加载真实常量的值
if os.environ.get('ENV', '') in ('production', 'dev'):
    from webspider.security_constants import *
