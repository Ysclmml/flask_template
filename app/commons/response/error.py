# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/6/12.
"""
from app.commons.response.exception import APIException

############################################
##########    基础类错误(0~9999)   ##########
############################################


class ServerError(APIException):
    code = 500
    error_code = 999
    msg = '服务器端异常'


class Failed(APIException):
    code = 400
    error_code = 9999
    msg = '失败'


############################################
########## 基础类错误(11000~12000) ##########
############################################

##########  权限相关(10000~10100)  ##########
class AuthFailed(APIException):
    code = 401
    error_code = 10000
    msg = '授权失败'


class Forbidden(APIException):
    code = 403
    error_code = 10010
    msg = '权限不足，禁止访问'


##########  查询相关(10100~10200)  ##########
class NotFound(APIException):
    code = 404  # http 状态码
    error_code = 10100  # 约定的异常码
    msg = '未查询到数据'  # 异常信息


class RepeatException(APIException):
    code = 400
    error_code = 10110
    msg = '重复数据'


class ParameterException(APIException):
    code = 400
    error_code = 10120
    msg = '参数错误'


########## Token相关(10200~10300) ##########
class TokenException(APIException):
    code = 401
    error_code = 10200
    msg = 'Token已过期或无效Token'


########## 文件相关(10300~10400) ##########
class FileTooLargeException(APIException):
    code = 413
    msg = '文件体积过大'
    error_code = 10310


class FileTooManyException(APIException):
    code = 413
    msg = '文件数量过多'
    error_code = 10320


class FileExtensionException(APIException):
    code = 401
    msg = '文件扩展名不符合规范'
    error_code = 10330


class QiniuExcepition(APIException):
    code = 401
    msg = '七牛云配置参数异常'
    error_code = 10350
