# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    __init__.py
   Author：       yscl
   date：         2020/12/3 14:46:07
   Description：  
  
-------------------------------------------------
"""
from flask import Blueprint

from app.api.v1.test_api import TestView
from app.commons.flask_request_mapping.route import register

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

register(api_v1, TestView)
