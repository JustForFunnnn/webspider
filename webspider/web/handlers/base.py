# coding: utf-8
from tornado.escape import json_encode
from tornado.web import RequestHandler

from webspider import constants
from webspider.exceptions import BaseException, ResourceNotFoundWebException
from webspider.web.formatter import Formatter
from webspider.utils.sql import remove_sessions


class BaseApiHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        exception = kwargs['exc_info'][1]

        # TODO 后端改成纯 API 后，删除其逻辑
        # 生产环境下, 且请求非 API 接口, 渲染错误页面
        if not constants.DEBUG and isinstance(self, BasePageHandler):
            self._handler_production_page_error(exception)
            return

        if isinstance(exception, BaseException):
            self.render_exception(exception)
        else:
            RequestHandler.write_error(self, status_code=status_code, **kwargs)

    def auto_render(self, data):
        formatted_dict = Formatter.format(data)
        self.render_json(formatted_dict)

    def _handler_production_page_error(self, exception):
        """处理生产环境下页面的错误"""
        if isinstance(exception, ResourceNotFoundWebException):
            self.render('404.html')
        else:
            self.render('500.html')

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

    def on_finish(self):
        remove_sessions()


# TODO page to api
class BasePageHandler(BaseApiHandler):
    """前后端代码混合型的页面 Handler"""
    pass
