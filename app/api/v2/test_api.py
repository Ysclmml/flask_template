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


@request_mapping('/test')
class TestView(MethodView):

    @request_mapping('/get/')
    def get_test(self):
        print("tttttt")
        return Success()




