# coding: utf-8
from tornado.escape import json_encode
from tornado.web import RequestHandler

from webspider.constants import DEBUG
from webspider.exceptions import BaseException, ResourceNotFoundException


class BaseHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        exception = kwargs['exc_info'][1]

        # TODO 后端改成纯 API 后，删除其逻辑
        # 生产环境下 且 页面为前后端混合型页面，渲染错误提示页面
        if not DEBUG and isinstance(self, BasePageHandler):
            if isinstance(exception, ResourceNotFoundException):
                self.render('404.html')
            else:
                self.render('500.html')
            return

        if isinstance(exception, BaseException):
            self.render_exception(exception)
        else:
            RequestHandler.write_error(self, status_code=status_code, **kwargs)

    def render_exception(self, exception):
        self.set_status(
            status_code=exception.STATUS_CODE,
            reason=exception.message
        )
        error_dict = {
            'error': {
                'code': exception.code,
                'name': exception.__class__.__name__,
                'message': exception.message,
                'data': exception.data if exception.data else '',
                'debug_message': exception.debug_message if exception.data else ''
            }
        }
        self.render_json(error_dict)

    def render_json(self, data):
        self.set_header('Content-Type', 'application/json')
        self.finish(json_encode(data))


# TODO page to api
class BasePageHandler(BaseHandler):
    """前后端代码混合型的页面 Handler"""
    pass
