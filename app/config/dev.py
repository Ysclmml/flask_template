# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    dev
   Author：       yscl
   date：         2020/12/2 13:49:35
   Description：  不一样的配置放在这里面
  
-------------------------------------------------
"""

DEBUG = True
SQLALCHEMY_ECHO = True


# 所有红图的路径
API_PATH = 'app.api'

ALL_RP_API_LIST = []

# 所有endpoint的meta信息
EP_META = {}
EP_INFO_LIST = []
EP_INFOS = {}

# 分页配置
PAGE_DEFAULT = 1
SIZE_DEFAULT = 10

# MySQL 数据库配置
# SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:root@192.168.101.113:3306/zerd?charset=utf8'
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:123456@47.102.148.156:3306/zerd?charset=utf8'
SQLALCHEMY_ENCODING = 'utf-8'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # 屏蔽 sql alchemy 的 FSADeprecationWarnin

# Redis配置
CACHE_SETTINGS = {
    'PREFIX': 'flask::temp::',
    'HOST': '127.0.0.1',
    'PORT': 6379,
    'db': 0
}
