# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    auth_utils
   Author：       yscl
   date：         2020/12/7 14:04:09
   Description：  
  
-------------------------------------------------
"""

import time
from collections import namedtuple
from functools import wraps

from flask import current_app, g, request
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired

from app.commons.cache.cache import BaseCache
from app.commons.response.error import AuthFailed, Forbidden
from app.dao.permission import PermissionDao
from app.models.permission import Role, User2Role, Permission, Role2Permission
from app.models.user import User

UserTuple = namedtuple('User', ['uid', 'ac_type', 'scope'])


def verity_auth_token(token):
    """校验用户的token, 并在g全局变量封装user对象, token, user_info, permissions"""
    # 校验token是否过期有效
    user_info = get_user_info_by_token(token)
    # 校验token是否在黑名单中
    if is_black_token(token):
        raise AuthFailed(msg='token无效', error_code=1002)
    g.user = User.get_or_404(id=user_info.uid)
    g.token = token
    g.user_info = user_info
    g.permissions = get_permissions_by_ids(user_info.scope)


def _decrypt_token(token):
    """解析token, 返回token的"""
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data, header = s.loads(token, return_header=True)  # token在请求头
    except BadSignature:
        raise AuthFailed(msg='token无效', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token过期', error_code=1003)
    return data, header


def get_user_info_by_token(token) -> UserTuple:
    """
    解析Token成UserTuple(uid, ac_type, scope)
    :param token:
    :return: UserTuple命名元祖(用户id, 用户登录类型, 用户的权限信息)
    """
    data, header = _decrypt_token(token)

    uid = data['uid']  # 用户ID
    ac_type = data['type']  # 登录方式
    scope = data['scope']  # 权限
    return UserTuple(uid, ac_type, scope)


def generate_auth_token(uid, ac_type, scope=None, expiration=None):
    """
    生成用户认证令牌
    @param uid: 用户id
    @param ac_type: 用户的登录类型, 定义为数字
    @param scope: 用户的权限信息, 存放权限的id列表
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


def set_black_list(token):
    """token设置黑名单"""
    key = 'auth_black::'
    data, header = _decrypt_token(token)
    # token的剩余有效时间
    remaining_time = (header.get('exp') - time.time()) / 3600
    BaseCache.prefix_client().set(f'{key}{token}', 1, remaining_time)


def is_black_token(token):
    """判断token是否在黑名单"""
    key = 'auth_black::'
    return BaseCache.prefix_client().get(f'{key}{token}') is not None


def get_permissions_by_ids(ids):
    """通过ids来获取用户的权限"""
    # todo: 这里的权限信息列表可以保存到缓存中
    return PermissionDao.get_permissions_name_by_ids(ids)


def get_permissions_name_by_uid(uid):
    """通过用户id来获取用户的权限名称列表"""
    permissions = PermissionDao.get_permissions_by_uid(uid)
    permissions = [permission.permission_name for permission in permissions]
    return permissions


def get_permissions_ids_by_uid(uid):
    """通过用户id来获取用户的权限id列表"""
    permissions = PermissionDao.get_permissions_by_uid(uid)
    permissions = [permission.id for permission in permissions]
    return permissions


def permissions_required(*permission_names):
    """权限装饰器"""

    def view_func(func):
        @wraps(func)
        def _wrapper(self, *args, **kwargs):
            if not g.user:
                raise AuthFailed(msg='token无效', error_code=1002)
            if not permission_names:
                # 登录就有访问权限
                return func(self, *args, **kwargs)
            if has_permissions(*permission_names):
                return func(self, *args, **kwargs)
            raise Forbidden()
        return _wrapper

    return view_func


def has_permissions(*permission_names):
    return bool(set(permission_names) & g.permissions)
