# coding=utf-8
from webspider.constants import JOB_JSON_URL
from webspider.utils.http_tools import requests_post, generate_http_request_headers


def get_jobs_count_from_lg(city_name, keyword_name):
    """
    爬取职位数量

    :param city_name: 城市名
    :param keyword_name: 关键词名
    :return: 城市下的关于关键词的职位数量,如北京的 python 职位数量
    :rtype: int
    """
    query_string = {'needAddtionalResult': False}
    if city_name != '全国':
        query_string['city'] = city_name
    form_data = {
        'first': False,
        'pn': 1,
        'kd': keyword_name
    }
    headers = generate_http_request_headers(
        referer='https://www.lg.com/jobs/list_java?labelWords=&fromSearch=true')
    response_json = requests_post(url=JOB_JSON_URL, params=query_string,
                                  data=form_data, headers=headers).json()
    return int(response_json['content']['positionResult']['totalCount'])
