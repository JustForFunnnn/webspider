# coding=utf-8

from sqlalchemy.exc import IntegrityError

from webspider.models.keyword import KeywordModel


def insert_keyword_if_not_exist(name):
    if KeywordModel.is_exist(filter_by={'name': name}):
        return
    try:
        keyword_id = KeywordModel.add(name=name)
        return keyword_id
    except IntegrityError:
        pass


def get_keyword_name_by_id(keyword_id):
    keyword = KeywordModel.get_by_pk(keyword_id)
    if not keyword:
        raise ValueError('Get None when keyword id is {}'.format(keyword_id))
    return keyword.name


def get_keyword_id_by_name(name):
    keyword = KeywordModel.get_one(filter_by={'name': name})
    if not keyword:
        raise ValueError('Get None when keyword name is {}'.format(name))
    return keyword.id
