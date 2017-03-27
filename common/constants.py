# coding=utf-8
import os

"""
    公司融资阶段
"""
FINANCE_STAGE_DICT = {
    'unknown': 0,
    '初创型(未融资)': 1,
    '初创型(天使轮)': 2,
    '成长型(A轮)': 3,
    '成长型(B轮)': 4,
    '成熟型(C轮)': 5,
    '成熟型(D轮及以上)': 6,
    '上市公司': 7,
    '成熟型(不需要融资)': 8,
    '成长型(不需要融资)': 9,
    '初创型(不需要融资)': 10
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
WORK_YEAR_DICT = {
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
EDUCATION_DICT = {
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

JOB_DETAIL_URL = 'https://www.lagou.com/jobs/{job_id}.html'

COMPANY_DETAIL_URL = 'https://www.lagou.com/gongsi/{company_id}.html'

ALL_CITY_URL = 'https://www.lagou.com/gongsi/allCity.html?option=0-0-0'

CITY_COMPANY_URL = 'https://www.lagou.com/gongsi/{city}-{finance_stage}-{industry}.json'

COMPANY_JOB_URL = 'https://www.lagou.com/gongsi/searchPosition.json'

"""
    其他常量
"""

DEBUG = (os.environ.get('DEPLOY_ENV', 'testing') == 'testing')

TEST_API = 'https://www.baidu.com/'

MIN_PROXY_COUNT = 30

HTTP_PROXY_FORMATTER = "http://{ip}:{port}"

HTTPS_PROXY_FORMATTER = "https://{ip}:{port}"

MIN_SLEEP_TIME = 3

MAX_SLEEP_TIME = 6

TIMEOUT = 5

# 用来设定最大的尝试次数，超过该次数就停止重试
RETRY_TIMES = 10
# 函数最久持续时间 单位: s
STOP_MAX_DELAY = 1000 * 60
# 设置在两次retrying之间的停留时间 单位:s
WAIT_FIXED = 1000 * 5

REDIS_PROXY_KEY = 'proxys'

REDIS_VISITED_COMPANY_KEY = 'visited_company'

"""
    HTTP 相关
"""
HTTP_SUCCESS = 200

HTTP_HEADER = {
    'Host': 'www.lagou.com',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Anit-Forge-Code': '0',
    'DNT': '1',
    'Referer': 'https//www.lagou.com/gongsi/',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4,en-US;q=0.2,en-GB;q=0.2',
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Origin': 'https//www.lagou.com',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Anit-Forge-Token': 'None',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'Cookie': "JSESSIONID=ABAAABAACEBACDG84DC9D7C2CB67134FCB262EAD8A32D95; _gat=1; user_trace_token=20170524154541-fc775956-4054-11e7-8d90-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_linux%2Bc%3Foquery%3DC%2B%2B%26fromSearch%3Dtrue%26labelWords%3Drelative; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fts%3D1495611939816%26serviceId%3Dlagou%26service%3Dhttps%25253A%25252F%25252Fwww.lagou.com%25252F%26action%3Dlogin%26signature%3D667D76BA15743B738600C3B9E5A110BC; LGUID=20170524154541-fc77609e-4054-11e7-8d90-5254005c3644; _putrc=BFF88537FC9713D8; login=true; unick=%E4%BD%95%E5%9B%BD%E6%9F%B1; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=80; TG-TRACK-CODE=index_hotsearch; SEARCH_ID=b33995ec33c34fb8bb8007ffd5b4c012; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.2334757.1495611966; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1495611941; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1495611966; _ga=GA1.2.1282538269.1495611941; LGSID=20170524154541-fc775c22-4054-11e7-8d90-5254005c3644; LGRID=20170524154606-0b242f06-4055-11e7-8d90-5254005c3"
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
