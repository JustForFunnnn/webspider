# coding=utf-8
import re
import json
import logging

from lxml import etree
from tornado.util import ObjectDict

from webspider import utils
from webspider import constants

logger = logging.getLogger(__name__)


def get_companies_pagination_from_lg(city_id=0, finance_stage_id=0, industry_id=0, page_no=1):
    """
    爬取公司分页数据

    :param city_id: 城市 id
    :param finance_stage_id: 融资阶段 id
    :param industry_id: 行业 id
    :param page_no: 页码
    :return: 公司分页数据
    :rtype: utils.pagination.Pagination
    """
    url = constants.COMPANIES_URL.format(city_id=city_id,
                                         finance_stage_id=finance_stage_id,
                                         industry_id=industry_id)

    params = {'pn': page_no, 'sortField': constants.SORTED_BY_JOBS_COUNT}
    response_json = utils.http_tools.requests_get(url=url, params=params).json()
    pagination = utils.pagination.Pagination(per_page=int(response_json['pageSize']),
                                             total=int(response_json['totalCount']))

    return pagination


def get_companies_from_lg(city_id=0, finance_stage_id=0, industry_id=0, page_no=1):
    """
    爬取公司数据

    返回的 dict 组成:
    lg_company_id:
        type: int
        meaning: 接口使用的公司 id
        eg: 1
    fullname:
        type: str
        meaning: 公司全称
        eg:  智者四海北京科技有限公司
    city_name:
        type: str
        meaning: 城市名
        eg: 北京
    shortname:
        type: str
        meaning: 公司简称
        eg: 知乎
    fullname:
        type: str
        meaning: 公司全称
        eg:  智者四海北京科技有限公司
    finance_stage:
        type: str
        meaning: 融资阶段
        eg:  D轮
    features:
        type: str
        meaning: 公司slogan, 一句话简介
        eg:  发现更大的世界
    process_rate:
        type:  int
        meaning:  简历处理率
        eg:  94
    industries:
        type: str
        meaning: 所处行业
        eg: '互联网，社交' or '互联网'
    advantage:
        type: List[str]
        meaning: 公司优势
        eg: ['双休', '五险一金', ......]
    address:
        type: str
        meaning: 公司地址
        eg: 北京市海淀区学院路768创意园
    size:
        type: str
        meaning: 公司规模
        eg: 2000人以上
    introduce:
        type: List[str]
        meaning: 公司介绍
        eg: ['我们的愿景:', 'blablabla', '我们处于一个知识 balala...']

    :param city_id: 城市 id
    :param finance_stage_id: 融资阶段 id
    :param industry_id: 行业 id
    :param page_no: 页码
    :return: 公司数据集合
    :rtype: List[tornado.util.ObjectDict]
    """
    url = constants.COMPANIES_URL.format(city_id=city_id,
                                         finance_stage_id=finance_stage_id,
                                         industry_id=industry_id)
    params = {'pn': page_no, 'sortField': constants.SORTED_BY_JOBS_COUNT}
    companies = utils.http_tools.requests_get(url=url, params=params).json()['result']

    companies_dicts = []
    for company in companies:
        lg_company_id = int(company.get('companyId'))

        company_detail = get_company_detail_from_lg(lg_company_id=lg_company_id)
        companies_dicts.append(ObjectDict(
            lg_company_id=lg_company_id,
            city_name=company.get('city'),
            shortname=company.get('companyShortName'),
            fullname=company.get('companyFullName'),
            finance_stage=company.get('financeStage'),
            features=company.get('companyFeatures'),
            process_rate=company.get('processRate'),
            industries=company.get('industryField'),
            # company detail
            advantage=company_detail.get('advantage'),
            address=company_detail.get('address'),
            size=company_detail.get('size'),
            introduce=company_detail.get('introduce')
        ))
    return companies_dicts


def get_company_detail_from_lg(lg_company_id):
    """
    爬取公司详情页的数据

    返回的 dict 组成:
    advantage:
        type: List[str]
        meaning: 公司优势
        eg: ['双休', '五险一金', ......]
    address:
        type: str
        meaning: 公司地址
        eg: 北京市海淀区学院路768创意园
    size:
        type: str
        meaning: 公司规模
        eg: 2000人以上
    introduce:
        type: List[str]
        meaning: 公司介绍
        eg: ['我们的愿景:', 'blablabla', '我们处于一个知识 balala...']

    :param lg_company_id: 接口使用的公司 id
    :return: 公司详情页数据
    :rtype: tornado.util.ObjectDict
    """
    response = utils.http_tools.requests_get(
        url=constants.COMPANY_DETAIL_URL.format(lg_company_id=lg_company_id))
    company_detail_html = etree.HTML(response.text)

    advantage = company_detail_html.xpath('//div[@id="tags_container"]//li/text()')
    sizes = company_detail_html.xpath('//div[@id="basic_container"]//li[3]/span/text()')
    address = company_detail_html.xpath('//p[@class="mlist_li_desc"]/text()')
    introduces = company_detail_html.xpath('//span[@class="company_content"]//text()')

    if not sizes:
        logger.error(
            'can not get size by lg_company_id = {}, html code is \n{}'.format(lg_company_id, response.text))

    return ObjectDict(
        advantage=advantage,
        address=address[0] if address else '',
        size=sizes[0] if sizes else '',
        introduce=introduces,
    )


def clean_lg_company_data(company_dict):
    """
    清洗爬取到的公司信息

    :param company_dict: tornado.util.ObjectDict
    """
    if 'size' in company_dict:
        company_dict.size = company_dict.size.strip()
    if 'finance_stage' in company_dict:
        company_dict.finance_stage = company_dict.finance_stage.strip()
    if 'features' in company_dict:
        company_dict.features = utils.text.to_plaintext(company_dict.features)
    if 'address' in company_dict:
        company_dict.address = utils.text.to_plaintext(company_dict.address)
    if 'introduce' in company_dict:
        company_dict.introduce = ''.join(company_dict.introduce) if company_dict.introduce else ''
        company_dict.introduce = company_dict.introduce[:constants.COMPANY_INTRODUCE_MAX_LEN]
    if 'advantage' in company_dict:
        company_dict.advantage = list(map(utils.text.to_plaintext, company_dict.advantage))
        company_dict.advantage = json.dumps(company_dict.advantage)[
            :constants.COMPANY_ADVANTAGE_MAX_LEN]
    if 'industries' in company_dict:
        company_dict.industries = set(re.split(r",|，|、|\s", company_dict.industries))
