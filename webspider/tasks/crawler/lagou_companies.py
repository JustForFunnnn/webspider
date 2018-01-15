# coding=utf-8
import re
import json
import logging

from lxml import etree
from tornado.util import ObjectDict

from webspider import utils
from webspider import constants
from webspider.controllers import city_ctl
from webspider.models import CompanyModel

logger = logging.getLogger(__name__)


def crawl_lagou_companies_pagination(city_id=0, finance_stage_id=0, industry_id=0, page_no=1):
    """
    获取拉勾公司 分页数据
    :param city_id: 城市 id, 默认 0 代表全国
    :param finance_stage_id: 融资阶段 id, 默认 0 代表全部阶段
    :param industry_id: 行业 id，默认 0 代表所有行业
    :return: utils.pagination.Pagination instance
    """
    # 生成访问链接
    url = constants.COMPANIES_URL.format(city_id=city_id,
                                         finance_stage_id=finance_stage_id,
                                         industry_id=industry_id)

    params = {'pn': page_no, 'sortField': constants.SORTED_BY_JOBS_COUNT}
    response_json = utils.http_tools.requests_get(url=url, params=params).json()
    pagination = utils.pagination.Pagination(per_page=int(response_json['pageSize']),
                                             total=int(response_json['totalCount']))

    return pagination


def crawl_lagou_companies(city_id=0, finance_stage_id=0, industry_id=0, page_no=1, skip_exist=True):
    """
    获取拉勾 公司数据
    :param city_id: 城市 id, 默认 0 代表全国
    :param finance_stage_id: 融资阶段 id, 默认 0 代表全部阶段
    :param industry_id: 行业 id，默认 0 代表所有行业
    :param page_no: 页码，默认爬取第1页数据
    :return: [
        {
            'lagou_company_id': 123,
            'city': '城市名',
            'shortname': '公司简称',
            'fullname': '公司全称',
            'finance_stage': '融资阶段',
            'features': '公司一句话简介',
            'process_rate': 62,
            'industries': '金融，医疗',
            'advantage': ['公司优势', 'blabla', ......],
            'address': '公司地址',
            'size': '公司规模',
            'introduce': ['公司详情', 'blabla']
        },
        .....
    ]
    """
    url = constants.COMPANIES_URL.format(city_id=city_id,
                                         finance_stage_id=finance_stage_id,
                                         industry_id=industry_id)
    params = {'pn': page_no, 'sortField': constants.SORTED_BY_JOBS_COUNT}
    response_json = utils.http_tools.requests_get(url=url, params=params).json()
    companies = response_json['result']

    companies_dicts = []
    for company in companies:
        lagou_company_id = int(company.get('companyId'))
        if skip_exist and CompanyModel.is_exist(filter_by={'lagou_company_id': lagou_company_id}):
            print('跳过 company, lagou company id is {}'.format(lagou_company_id))
            continue

        company_detail = crawl_lagou_company_detail(lagou_company_id=lagou_company_id)
        companies_dicts.append(ObjectDict(
            lagou_company_id=lagou_company_id,
            city=company.get('city'),
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


def crawl_lagou_company_detail(lagou_company_id):
    """
    爬取拉勾 公司详情页数据
    :param lagou_company_id: 拉勾的 company id
    :return: [
        {
            'advantage': '公司优势',
            'address': '公司地址',
            'size': '公司规模' ,
            'introduce': ['公司详情', 'blabla']
        },
        .....
    ]
    """
    response = utils.http_tools.requests_get(url=constants.COMPANY_DETAIL_URL.format(lagou_company_id=lagou_company_id))
    company_detail_html = etree.HTML(response.text)

    advantage = company_detail_html.xpath('//div[@id="tags_container"]//li/text()')
    sizes = company_detail_html.xpath('//div[@id="basic_container"]//li[3]/span/text()')
    address = company_detail_html.xpath('//p[@class="mlist_li_desc"]/text()')
    introduces = company_detail_html.xpath('//span[@class="company_content"]//text()')

    if not sizes:
        logger.error('can not get size by lagou_company_id = {}'.format(lagou_company_id))

    return ObjectDict(
        advantage=advantage,
        address=address[0] if address else '',
        size=sizes[0] if sizes else '',
        introduce=introduces,
    )


def clean_lagou_company_data(company_dict):
    """
    清洗爬取到的拉勾公司信息
    company_dict.features: 去除多余空格，换行符号
    company_dict.industries: '金融，医疗' -> ['金融', '医疗']
    company_dict.address: 去除多余空格，换行符号
    company_dict.introduce: ['公司详情, ', 'blabla'] -> '公司详情, blabla'
    company_dict.advantage: 去除多余空格，换行符号
    company_dict.finance_stage: 去除前后空格
    company_dict.size: 去除前后空格
    """
    if 'size' in company_dict:
        company_dict.size = company_dict.size.strip()
    if 'finance_stage' in company_dict:
        company_dict.finance_stage = company_dict.finance_stage.strip()
    if 'features' in company_dict:
        company_dict.features = utils.text.to_plaintext(company_dict.features)
    if 'industries' in company_dict:
        company_dict.industries = set(re.split(r",|，|、", company_dict.industries))
    if 'address' in company_dict:
        company_dict.address = utils.text.to_plaintext(company_dict.address)
    if 'introduce' in company_dict:
        company_dict.introduce = ''.join(company_dict.introduce) if company_dict.introduce else ''
        company_dict.introduce = company_dict.introduce[:constants.COMPANY_INTRODUCE_MAX_LEN]
    if 'advantage' in company_dict:
        company_dict.advantage = list(map(utils.text.to_plaintext, company_dict.advantage))
        company_dict.advantage = json.dumps(company_dict.advantage)[:constants.COMPANY_ADVANTAGE_MAX_LEN]


def convert_lagou_company_data(company_dict):
    """
    爬取到公司信息 转换为 可以存储到数据库的数据
    company_dict.advantage array -> json
    company_dict.finance_stage str -> int(constants.FINANCE_STAGE_DICT)
    company_dict.size -> str -> int(constants.COMPANY_SIZE_DICT)

    add:
    company_dict.city_id: city_name -> city_id
    """
    if company_dict.finance_stage not in constants.FINANCE_STAGE_DICT:
        logger.error(
            '{} not in constants.FINANCE_STAGE_DICT, lagou company id is {}'.format(company_dict.finance_stage,
                                                                                    company_dict.lagou_company_id))
    company_dict.finance_stage = constants.FINANCE_STAGE_DICT.get(company_dict.finance_stage,
                                                                  constants.FINANCE_STAGE_DICT['unknown'])

    if company_dict.size not in constants.COMPANY_SIZE_DICT:
        logger.error(
            '{} not in constants.COMPANY_SIZE_DICT, lagou company id is {}'.format(company_dict.size,
                                                                                   company_dict.lagou_company_id))
    company_dict.size = constants.COMPANY_SIZE_DICT.get(company_dict.size, constants.COMPANY_SIZE_DICT['unknown'])

    company_dict.city_id = city_ctl.get_city_id_by_name(company_dict.city)
