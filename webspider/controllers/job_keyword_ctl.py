# -*- coding: utf-8 -*-
from sqlalchemy import func

from webspider.models.job_keyword import JobKeywordModel


def get_most_frequently_keyword_ids(limit=None, offset=None):
    """
    获得出现最为频繁的关键词 id
    :param limit:
    :param offset:
    :return: 关键词 id 集合
    :rtype: List[int]
    """
    result = JobKeywordModel.list(columns=JobKeywordModel.keyword_id, group_by=JobKeywordModel.keyword_id,
                                  order_by=func.count(JobKeywordModel.id).desc(), limit=limit, offset=offset)
    return [item[0] for item in result]
