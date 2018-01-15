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
    拉勾相关网页
"""

JOB_JSON_URL = 'https://www.lagou.com/jobs/positionAjax.json'

JOB_DETAIL_URL = 'https://www.lagou.com/jobs/{lagou_job_id}.html'

COMPANY_DETAIL_URL = 'https://www.lagou.com/gongsi/{lagou_company_id}.html'

ALL_CITY_URL = 'https://www.lagou.com/gongsi/allCity.html?option=0-0-0'

COMPANIES_URL = 'https://www.lagou.com/gongsi/{city_id}-{finance_stage_id}-{industry_id}.json'

COMPANY_JOBS_URL = 'https://www.lagou.com/gongsi/searchPosition.json'

# COMPANIES_URL sort field
SORTED_BY_JOBS_COUNT = 1

"""
    其他常量
"""

DEBUG = (os.environ.get('DEPLOY_ENV', 'dev') == 'dev')

MIN_PROXY_COUNT = 30

HTTP_PROXY_FORMATTER = "http://{ip}:{port}"

HTTPS_PROXY_FORMATTER = "https://{ip}:{port}"

TIMEOUT = 4

SLEEP_SECS = 4

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
    HTTP 相关 
"""
HTTP_HEADER = {}

USER_AGENT_LIST = {}