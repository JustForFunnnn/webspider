# coding: utf-8
import traceback

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def prepare(self):
        super(BaseHandler, self).prepare()

    def on_finish(self):
        super(BaseHandler, self).on_finish()

    def write_error(self, status_code, **kwargs):
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
        else:
            if status_code == 404:
                self.render('404.html')
            else:
                self.render('500.html')

    def get(self, *args, **kwargs):
        self.write_error(404)
