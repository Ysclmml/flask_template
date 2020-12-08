# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    base
   Author：       yscl
   date：         2020/12/2 13:52:48
   Description：  公共的配置可以放在这里面
  
-------------------------------------------------
"""
import os
from datetime import datetime

SECRET_KEY = 'abcdevadafdasfkljasdfjk'
TOKEN_EXPIRE = 3600 * 7 * 24  # token过期时间, 当前为7天
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




