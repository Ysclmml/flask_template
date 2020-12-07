# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    permission
   Author：       yscl
   date：         2020/12/7 17:11:55
   Description：  
  
-------------------------------------------------
"""
from app.models.permission import Role, Permission, Role2Permission, User2Role


class PermissionDao(object):

    @staticmethod
    def get_permissions_by_uid(uid):
        """通过用户id来获取用户的权限"""
        roles = Role.query.with_entities(Role.id).join(User2Role).filter(User2Role.user_id == uid)
        # 通过roles_id来获取权限
        roles = [role[0] for role in roles]
        permissions = Permission.query.join(
            Role2Permission).filter(
            Role2Permission.role_id.in_(roles)).distinct()
        return list(permissions)

    @staticmethod
    def get_permissions_name_by_ids(ids):
        permissions = Permission.query.with_entities(Permission.permission_name).filter(Permission.id.in_(ids))
        permissions = [permission[0] for permission in permissions]
        return permissions
