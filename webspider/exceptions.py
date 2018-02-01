# !/usr/bin/env python
# -*- coding: utf-8 -*-
__all__ = ['BaseException', 'ResourceNotFoundException']


class BaseException(Exception):
    ERROR_CODE = None
    STATUS_CODE = 200

    def __init__(self, message, data=None, debug_message=None):
        if self.ERROR_CODE is None:
            raise NotImplementedError()
        self._message = message
        self._data = dict(data) if data else None
        self._debug_message = debug_message

    @property
    def code(self):
        return self.ERROR_CODE

    @property
    def message(self):
        return self._message

    @property
    def data(self):
        return self._data

    @property
    def debug_message(self):
        return self._debug_message

    def __str__(self):
        return "Exception: code={code}, message={message}, data={data}, debug_message={debug_message}".format(
            code=self.code, message=self.message, data=self.data, debug_message=self.debug_message)

    def __repr__(self):
        return self.__str__()


class ResourceNotFoundException(BaseException):
    """
    Corresponding to HTTP code 404
    """
    ERROR_CODE = 4041
    STATUS_CODE = 404

    def __init__(self, message=u'资源不存在', data=None, debug_message=None):
        super(ResourceNotFoundException, self).__init__(message, data, debug_message)
