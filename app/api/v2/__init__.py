# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    __init__.py
   Author：       yscl
   date：         2020/12/3 15:05:35
   Description：  
  
-------------------------------------------------
"""
from flask import Blueprint

from app.api.v2.test_api import TestView
from app.commons.flask_request_mapping.route import register

api_v2 = Blueprint('api_v2', __name__, url_prefix='/api/v2')

register(api_v2, TestView)
