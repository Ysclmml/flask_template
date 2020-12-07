""" 
@Function:
@Author  : ybb
@Time    : 2020/9/28 18:10
"""
from app.commons.response.error import ParameterException


class ValidException(ParameterException):
    """自定义校验异常"""
    def __init__(self, message='ValidException'):
        self.message = message
        super().__init__(msg=message)


class FieldValidException(ParameterException):
    """自定义字段校验异常"""
    def __init__(self, message='FieldValidException'):
        self.message = message
        super().__init__(msg=message)
