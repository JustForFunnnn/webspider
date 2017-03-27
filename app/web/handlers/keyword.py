# coding: utf-8
from app.web.handlers.base import BaseHandler
from app.controllers.keyword import KeywordController


class KeywordHandler(BaseHandler):
    def get(self):
        keyword_name = self.get_argument('keyword')
        keyword = KeywordController.get(name=keyword_name)
        if not keyword:
            self.write_error(404)
        (work_year_dict, education_dict, city_dict, salary_dict, finance_stage_dict) \
            = KeywordController.keyword_analyze(keyword_id=keyword.id)
        self.render("keyword.html",
                    keyword=keyword_name,
                    work_year_dict=work_year_dict,
                    education_dict=education_dict,
                    city_dict=city_dict,
                    salary_dict=salary_dict,
                    finance_stage_dict=finance_stage_dict)
