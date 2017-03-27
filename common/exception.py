# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BaseError(Exception):
    def __init__(self, code=None, message=None, error_log=None):
        self._code = code
        self._message = message
        self._error_log = error_log

    def __str__(self):
        return "Exception: code={0}, message={1}, error_log={2}".format(
            self._code, self._message, self._error_log)

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return u"Exception: code={0}, message={1}, error_log={2}".format(
            self._code, self._message, self._error_log)


class ProxyCountError(BaseException):
    def __init__(self, message=u'代理数量过少', error_log=None):
        super(ProxyCountError, self).__init__(100001, message, error_log)


class ProxyFormatterError(BaseException):
    def __init__(self, message=u'代理格式错误', error_log=None):
        super(ProxyFormatterError, self).__init__(100001, message, error_log)


class RequestsError(BaseException):
    def __init__(self, message=u'请求网页出错', error_log=None):
        super(RequestsError, self).__init__(100001, message, error_log)
