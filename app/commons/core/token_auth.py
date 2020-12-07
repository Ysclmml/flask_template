# _*_ coding: utf-8 _*_
"""
  Created by Allen7D on 2018/6/13.
"""
from collections import namedtuple
from functools import wraps

from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth as _HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired

from app.commons.response.error import AuthFailed
from app.models.user import User

UserTuple = namedtuple('User', ['uid', 'ac_type', 'scope'])


def verity_auth_token(token):
    """校验用户的token, 并在g全局变量封装user对象, token, user_info"""
    user_info = decrypt_token(token)
    g.user = User.get_or_404(id=user_info.uid)
    g.token = token
    g.user_info = user_info


def decrypt_token(token) -> UserTuple:
    """
    解析Token成UserTuple(uid, ac_type, scope)
    :param token:
    :return: UserTuple命名元祖(用户id, 用户登录类型, 用户的权限信息)
    """
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)  # token在请求头
    except BadSignature:
        raise AuthFailed(msg='token无效', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token过期', error_code=1003)
    uid = data['uid']  # 用户ID
    ac_type = data['type']  # 登录方式
    scope = data['scope']  # 权限
    return UserTuple(uid, ac_type, scope)


def generate_auth_token(uid, ac_type, scope=None, expiration=None):
    """
    生成用户认证令牌
    @param uid: 用户id
    @param ac_type: 用户的登录类型, 定义为数字
    @param scope: 用户的权限信息
    @param expiration: token的过期时间设置, 优先从参数中获取, 然后从配置文件获取, 都不设置默认7200s
    @return: token
    """
    expiration = expiration or current_app.config.get('TOKEN_EXPIRE', 7200)
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({
        'uid': uid,
        'type': ac_type,
        'scope': scope
    })
    return token.decode()
