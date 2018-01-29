# # # -*- coding: utf-8 -*-
#
#
# def update_salary_dict(salary_dict, start, end):
#     if len(salary_dict) == 0:
#         salary_dict = {i: 0 for i in range(0, 111)}
#     for index in range(start, end + 1):
#         salary_dict[index] += 1
#     return salary_dict
#
#
# def get_salary_section(string):
#     """
#     e.g:
#     15k-25k  ->  (15, 25)
#     15k以上  ->  (15, 20)
#     15k以下  ->  (10, 15)
#     :param string: 15k-25k
#     :return: 15,25
#     """
#     pattern = r'K|k|以上|以下'
#     replace_char = ''
#
#     if string.find('-') != -1:
#         string = re.sub(pattern=pattern, repl=replace_char, string=string)
#         start, end = string.split('-')
#     elif string.endswith('以下'):
#         string = re.sub(pattern=pattern, repl=replace_char, string=string)
#         start, end = int(string) - 5 if int(string) - 5 >= 0 else 1, string
#     elif string.endswith('以上'):
#         string = re.sub(pattern=pattern, repl=replace_char, string=string)
#         start, end = string, int(string) + 5
#     else:
#         raise Exception('error salary' + string)
#
#     return int(start), int(end)
#
# from webspider.utils.util import reverse_dict
# from webspider.utils.util import get_salary_section
# from webspider.utils.time_tools import timestamp2string
# from webspider.utils.cache import simple_cache
#
# # class JobController(object):
# #     @classmethod
# #     def add(cls, id, company_id, city_id, title, work_year='', department='', salary='', education='', description='',
# #             advantage='', nature='', created_at=0):
# #         JobModel.add(id=id, title=title, city_id=city_id, company_id=company_id, work_year=work_year,
# #                      department=department, salary=salary, education=education, description=description,
# #                      advantage=advantage, nature=nature, created_at=created_at)
# #
# #     @classmethod
# #     def count(cls, id=None, keyword_id=None):
# #         return JobModel.count(id=id, keyword_id=keyword_id)
# #
# #     @classmethod
# #     def list(cls, keyword_id=None, limit=None, offset=None):
# #         return JobModel.list(keyword_id=keyword_id, limit=limit, offset=offset)
# #
#
# def work_years_request_analyze(jobs):
#     """分析职位的工作年限要求"""
#     reversed_word_years_request_dict = reverse_dict(constants.WORK_YEARS_REQUEST_DICT)
#     work_years_request_counter = {}
#     for job in jobs:
#         work_years_request = reversed_word_years_request_dict[job.work_year]
#         if work_years_request in work_years_request_counter:
#             work_years_request_counter[work_years_request] += 1
#         else:
#             work_years_request_counter[work_years_request] = 1
#     return work_years_request_counter
#
#
# def educations_request_analyze(jobs):
#     """分析职位的学历要求"""
#     reversed_education_request_dict = reverse_dict(constants.EDUCATION_REQUEST_DICT)
#     educations_request_counter = {}
#     for job in jobs:
#         education_request = reversed_education_request_dict[job.education]
#         if education_request in educations_request_counter:
#             educations_request_counter[education_request] += 1
#         else:
#             educations_request_counter[education_request] = 1
#     return educations_request_counter
#
#
# def finance_stage_distribution_analyze(jobs):
#     """分析招聘该职位的公司的融资分布情况"""
#     company_ids = [job.company_id for job in jobs]
#     companys = CompanyController.list(ids=company_ids)
#
#     reversed_finance_stage_dict_dict = reverse_dict(constants.FINANCE_STAGE_DICT)
#     # 特定排序的融资dict
#     finance_stage_distribution = {
#         '成熟型(不需要融资)': 0,
#         '成长型(不需要融资)': 0,
#         '初创型(不需要融资)': 0,
#         '上市公司': 0,
#         '成熟型(D轮及以上)': 0,
#         '成熟型(C轮)': 0,
#         '成长型(B轮)': 0,
#         '成长型(A轮)': 0,
#         '初创型(天使轮)': 0,
#         '初创型(未融资)': 0,
#     }
#     for company in companys:
#         finance_stage = reversed_finance_stage_dict_dict[company.finance_stage]
#         if finance_stage in finance_stage_distribution:
#             finance_stage_distribution[finance_stage] = finance_stage_distribution[finance_stage] + 1
#     return finance_stage_distribution
#
#
# def city_job_quantity_analyze(jobs, limit=10):
#     """统计各城市的招聘职位的数量"""
#     city_job_quantityer = {}
#     city_name_dict = CityController.get_city_name_dict()
#     for job in jobs:
#         city_name = city_name_dict[job.city_id]
#         city_job_quantityer[city_name] = city_job_quantityer[city_name] + 1 if city_name in city_job_quantityer else 1
#     city_job_quantityer = sorted(city_job_quantityer.items(), key=lambda x: x[1], reverse=True)[:limit]
#     return city_job_quantityer
#
#
# def salary_distribution_analyze(jobs):
#     """分析职位的薪水分布情况"""
#     salary_distribution = {
#         '10k 及以下': 0,
#         '11k-20k': 0,
#         '21k-35k': 0,
#         '36k-60k': 0,
#         '61k 以上': 0
#     }
#     for job in jobs:
#         start_salary, end_salary = get_salary_section(job.salary)
#         if start_salary <= 10:
#             salary_distribution['10k 及以下'] += 1
#         if start_salary <= 20 and end_salary >= 11:
#             salary_distribution['11k-20k'] += 1
#         if start_salary <= 35 and end_salary >= 21:
#             salary_distribution['21k-35k'] += 1
#         if start_salary <= 60 and end_salary >= 36:
#             salary_distribution['36k-60k'] += 1
#         if end_salary >= 61:
#             salary_distribution['61k 以上'] += 1
#     return salary_distribution
#
#
# @simple_cache
# def get_jobs_statistics(keyword_id):
#     keyword_job_quantity = JobsCountController.list(keyword_id=keyword_id, sort_by='asc')
#     for item in keyword_job_quantity:
#         item.date_string = timestamp2string(timestamp=item.date, date_format='%m/%d')
#     jobs = JobModel.list(filter_by={'keyword_id': keyword_id})
#     educations_request_counter = educations_request_analyze(jobs=jobs)
#     finance_stage_distribution = finance_stage_distribution_analyze(jobs=jobs)
#     city_job_quantityer = city_job_quantity_analyze(jobs=jobs)
#     salary_distribution = salary_distribution_analyze(jobs=jobs)
#     work_years_request = work_years_request_analyze(jobs=jobs)
#     return (keyword_job_quantity,
#             educations_request_counter,
#             finance_stage_distribution,
#             city_job_quantityer,
#             salary_distribution,
#             work_years_request)
