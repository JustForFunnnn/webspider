# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TIMESTAMP

from webspider import constants
from webspider.models.base import BaseModel


class JobExtraModel(BaseModel):
    __tablename__ = 'job_extra'

    job_id = Column(INTEGER, nullable=False, primary_key=True)
    description = Column(VARCHAR(constants.JOB_DESCRIPTION_MAX_LEN), nullable=False, doc=u'额外描述')
    advantage = Column(VARCHAR(constants.JOB_ADVANTAGE_MAX_LEN), nullable=False, doc=u'职位优势')
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now, doc=u'创建时间')
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'创建时间')
