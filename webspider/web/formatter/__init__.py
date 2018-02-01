# coding=utf-8
from webspider.models import KeywordStatisticModel, JobsCountModel
from webspider.web.formatter.jobs_count import JobsCountFormatter
from webspider.web.formatter.keyword_statistic import KeywordStatisticFormatter

from webspider.web.formatter.base import Formatter

formatter_mappings = {
    JobsCountModel: JobsCountFormatter,
    KeywordStatisticModel: KeywordStatisticFormatter,
}

Formatter.register_formatter(formatter_mappings)
