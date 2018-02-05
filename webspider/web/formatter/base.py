# coding=utf-8
from tornado.util import ObjectDict

from webspider.exceptions import DowngradeException


class Downgrade(object):
    """降级"""
    def __init__(self, value):
        self.value = value


class Field(object):
    """Formatter字段"""
    def __init__(self, name, converter=None, downgrade=None):
        self.name = name
        self.converter = converter
        if downgrade is not None and not isinstance(downgrade, Downgrade):
            raise DowngradeException(u'downgrade must be Downgrade instance')
        self.downgrade = downgrade


class Formatter(object):
    """Formatter 根据设定的 FORMATTER_MAPS 自动渲染"""
    _FORMATTER_MAPS = {}
    FIELDS = {}

    @classmethod
    def register_formatter(cls, mapping):
        cls._FORMATTER_MAPS.update(mapping)

    @classmethod
    def format(cls, data):
        if isinstance(data, list):
            return [cls.format(item) for item in data]
        else:
            formatter = cls.get_formatter(data)
            if not formatter:
                raise ValueError(u'Can not find the formatter by model {}'.format(type(data)))

            format_result = ObjectDict()
            for field in formatter.FIELDS:
                if not isinstance(field, Field):
                    raise ValueError('formatter field must be Field instance')
                try:
                    value = getattr(data, field.name)
                    # 可再次渲染
                    if isinstance(value, list) or cls.get_formatter(value):
                        value = cls.format(value)
                    if field.converter:
                        value = field.converter(value)
                except Exception:
                    # Field 设置了降级
                    if field.downgrade:
                        value = field.downgrade.value
                    else:
                        raise
                format_result[field.name] = value

            return format_result

    @classmethod
    def get_formatter(cls, data):
        if data in cls._FORMATTER_MAPS:
            return cls._FORMATTER_MAPS[data]
        for model, formatter in cls._FORMATTER_MAPS.items():
            if type(data) is model:
                return formatter
