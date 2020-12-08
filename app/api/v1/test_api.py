# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    test
   Author：       yscl
   date：         2020/12/2 15:31:11
   Description：  
  
-------------------------------------------------
"""
from flask import request
from flask.views import MethodView

from app.commons.flask_request_mapping.mapping import request_mapping
from app.commons.response.ok import Success
# from app.dao.user import UserDao
from app.dao.user import UserDao

from app.validation.field_validation import *
from app.validation.base_validation import BaseValidation

import logging
logger = logging.getLogger('flask')


class Test():

    name = [NotEmpty()]
    age = [NotEmpty(), NumRange(18, 24)]

    def validate(self, attrs):
        attrs.update(age=99)
        return attrs


@request_mapping('/test')
class TestView(MethodView):

    @request_mapping('/get/', method='post')
    @BaseValidation(Test)
    def get_test(self):
        print(request.get_json())
        # user = UserDao.get_first()
        return Success('ok')

    @request_mapping('/post', method='post')
    def post_test(self):
        UserDao.create_user()
        return Success()

    @request_mapping('/getRel/', method='get')
    def get_rel(self):
        user = UserDao.relation_test()
        logger.info('get_rel..........')
        return Success(user)




