# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    ok
   Author：       yscl
   date：         2020/12/2 14:11:43
   Description：  
  
-------------------------------------------------
"""
import json

from app.commons.response.exception import APIException
from app.commons.utils.common_utils import jsonify


class Success(APIException):
    """
    0/200: 查询成功
    1/201: 创建 | 更新成功
    2/203: 删除成功
    """
    code = 200
    error_code = 0
    data = None
    msg = '成功'

    def __init__(self, data=None, code=None, error_code=None, msg=None):
        if data:
            self.data = jsonify(data)
        if error_code == 1:
            code = code if code else 201
            msg = msg if msg else '创建 | 更新成功'
        if error_code == 2:
            code = code if code else 202
            msg = msg if msg else '删除成功'
        super(Success, self).__init__(code, error_code, msg)

    def get_body(self, environ=None):
        body = dict(
            error_code=self.error_code,
            msg=self.msg,
            data=self.data
        )
        text = json.dumps(body)  # 返回文本
        return text
