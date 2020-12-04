# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    __init__.py
   Author：       yscl
   date：         2020/12/2 11:42:34
   Description：  
  
-------------------------------------------------
"""
from flask import Flask
from .v1 import api_v1
from .v2 import api_v2


def register_blueprint(app: Flask):
    """注册蓝图与路由"""
    app.register_blueprint(api_v1)
    app.register_blueprint(api_v2)

