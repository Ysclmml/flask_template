# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    test
   Author：       yscl
   date：         2020/12/2 15:31:11
   Description：  
  
-------------------------------------------------
"""

from flask.views import MethodView

from app.commons.flask_request_mapping.mapping import request_mapping
from app.commons.response.ok import Success
from app.dao.user import UserDao


@request_mapping('/test')
class TestView(MethodView):

    @request_mapping('/get/')
    def get_test(self):
        user = UserDao.get_first()
        return Success(user)

    @request_mapping('/post', method='post')
    def post_test(self):
        UserDao.create_user()
        return Success()

    @request_mapping('/getRel/', method='get')
    def get_rel(self):
        user = UserDao.relation_test()
        return Success(user)




