# coding=utf-8
# flake8: noqa
import os

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
    '全职': 0,
    '兼职': 1,
    '实习': 2,
}

"""
     工作年限要求
"""
WORK_YEARS_REQUEST_DICT = {
    'unknown': 0,
    '1-3年': 1,
    '10年以上': 2,
    '3-5年': 3,
    '5-10年': 4,
    '不限': 5,
    '应届毕业生': 6,
    '1年以下': 7,
}

"""
     学历要求
"""
EDUCATION_REQUEST_DICT = {
    '不限': 0,
    '博士': 1,
    '大专': 2,
    '本科': 3,
    '硕士': 4,
}

"""
    公司规模
"""
COMPANY_SIZE_DICT = {
    'unknown': 0,
    '15-50人': 1,
    '50-150人': 2,
    '150-500人': 3,
    '500-2000人': 4,
    '2000人以上': 5,
    '少于15人': 6,
}

"""
    拉勾相关网页
"""

JOB_JSON_URL = 'https://www.lagou.com/jobs/positionAjax.json'

JOB_DETAIL_URL = 'https://www.lagou.com/jobs/{lagou_job_id}.html'

COMPANY_DETAIL_URL = 'https://www.lagou.com/gongsi/{lagou_company_id}.html'

ALL_CITY_URL = 'https://www.lagou.com/gongsi/allCity.html?option=0-0-0'

COMPANIES_URL = 'https://www.lagou.com/gongsi/{city_id}-{finance_stage_id}-{industry_id}.json'

COMPANY_JOB_URL = 'https://www.lagou.com/gongsi/searchPosition.json'

# COMPANIES_URL sort field
SORTED_BY_JOBS_COUNT = 1

"""
    其他常量
"""

DEBUG = (os.environ.get('DEPLOY_ENV', 'dev') == 'dev')

TEST_API = 'https://www.baidu.com/'

MIN_PROXY_COUNT = 30

HTTP_PROXY_FORMATTER = "http://{ip}:{port}"

HTTPS_PROXY_FORMATTER = "https://{ip}:{port}"

MIN_SLEEP_TIME = 4

MAX_SLEEP_TIME = 7

TIMEOUT = 4

SLEEP_SECS = 4

SECONDS_OF_DAY = 60 * 60 * 24

REDIS_PROXY_KEY = 'proxys'

REDIS_VISITED_COMPANY_KEY = 'visited_company'

REDIS_VISITED_PEOPLES_COUNT_KEY = 'visited_peoples_count'

CACHE_SIZE = 128

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
HTTP_SUCCESS = 200

HTTP_HEADER = {
    'Host': 'www.lagou.com',
    'Referer': 'https://www.lagou.com/gongsi/',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Anit-Forge-Code': '0',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4,en-US;q=0.2,en-GB;q=0.2',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Origin': 'https//www.lagou.com',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': 'None',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'Cookie': 'user_trace_token=20171228200800-a343a41c-2539-4034-a0f0-54d164d0ba60; JSESSIONID=ABAAABAACDBABJB1A79D194CD92AFB65C0CFD6177D3294C; _ga=GA1.2.576047458.1514462908; LGUID=20171228200827-d00abdea-ebc7-11e7-b38b-525400f775ce; index_location_city=%E5%B9%BF%E5%B7%9E; TG-TRACK-CODE=index_search; SEARCH_ID=bae02c75722541cf93acd00963a325f4; X_HTTP_TOKEN=20c35481282abe6b14aa0b61535ab01d; LGSID=20171229154521-38d00008-ec6c-11e7-b6bd-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; _gat=1; LGRID=20171229155656-d6fe110f-ec6d-11e7-9f67-5254005c3644'
}

USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20120101 Firefox/29.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/29.0",
    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
    "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
    "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
    "Mozilla/5.0 (Windows NT 6.3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 360Browser"
]
