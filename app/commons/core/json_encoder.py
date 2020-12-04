# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    json_encoder
   Author：       yscl
   date：         2020/12/2 14:30:03
   Description：  
  
-------------------------------------------------
"""
from datetime import date, datetime
from flask.json import JSONEncoder as _JSONEncoder


class JSONEncoder(_JSONEncoder):
    def default(self, obj):
        # 如果obj是数据库查询获得的实例对象
        if hasattr(obj, 'keys') and hasattr(obj, '__getitem__'):
            obj.lock_fields()  # 锁定ctrl层的hide过和append过的字段
            return dict(obj)
        # 如果o是时间戳
        # datetime.now() ==> datetime.datetime(2020, 4, 8, 9, 4, 57, 26881)
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%dT%H:%M:%SZ')
        # date.today() ==> datetime.date(2020, 4, 8)
        if isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return super().default(obj)
