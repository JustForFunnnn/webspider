# coding=utf-8
import logging

from webspider import constants

logger = logging.getLogger(__name__)

CONSTANTS_MAP = {
    'finance_stage': constants.FINANCE_STAGE_DICT,
    'nature': constants.JOB_NATURE_DICT,
    'work_year': constants.WORK_YEARS_REQUEST_DICT,
    'education': constants.EDUCATION_REQUEST_DICT,
    'size': constants.COMPANY_SIZE_DICT,
}


def convert_dict_field_to_constants(to_converted_dict, constants_map=CONSTANTS_MAP):
    """
    把dict的字段转换为相应常量
    :param to_converted_dict: 需要转换的字典
    :param constants_map: 字段常量对应关系
    :return: 转换后的字段
    """
    for field_name, field_value in to_converted_dict.items():
        if field_name in constants_map:
            to_converted_dict[field_name] = convert_field_to_constants(field_name, field_value, constants_map)


def convert_field_to_constants(field_name, field_value, constants_map=CONSTANTS_MAP):
    """
    把字段转化为相应的常量, 如果无法转换，返回 -1

    eg:
        convert_field_to_constants(field_name='size', field_value='2000人以上', constants_map={'size': {'2000人以上': 1}})
        return: 1
    :param field_name: 字段名
    :param field_value: 字段值
    :param constants_map: 字段常量对应关系
    :rtype: int
    """
    if field_name not in constants_map:
        raise ValueError(u'can not find the field in constants_map, field name is {}'.find(field_name))

    field_constant_map = constants_map[field_name]

    if field_value in field_constant_map:
        return field_constant_map[field_value]
    else:
        logger.error('error {field_name}, value is {field_value}'.format(field_name=field_name,
                                                                         field_value=field_value))
        return field_constant_map['unknown'] if 'unknown' in field_constant_map else -1
