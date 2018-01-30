# coding=utf-8
import logging
from collections import Counter

logger = logging.getLogger(__name__)


def get_key_from_dict_by_value(value, dictionary):
    keys = [_key for (_key, _value) in dictionary.items() if _value == value]
    if not keys:
        raise ValueError(u'can not get key from dict by value {}'.format(value))
    if len(keys) > 1:
        raise ValueError(u'get multi keys from dict by value {}'.format(value))
    return keys[0]


def get_field_statistics(values, constants_dict):
    """
    获得某批数据的统计情况
    eg:
        input:
            constants_dict = {'男': 0, '女': 1}
            values = [0, 0, 0, 1, 1]
        return:
            {'男':3, '女':2}

    :param values: list[int], field values list
    :param constants_dict: Dict
    :return: collections.Counter
    """
    statistics_counter = Counter()
    for value in values:
        field_name = get_key_from_dict_by_value(value=value, dictionary=constants_dict)
        statistics_counter[field_name] += 1
    return statistics_counter
