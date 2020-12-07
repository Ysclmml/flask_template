# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    permission
   Author：       yscl
   date：         2020/12/7 13:31:49
   Description：  
  
-------------------------------------------------
"""
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, SmallInteger
from sqlalchemy.orm import relationship

from app.commons.core.db import EntityModel, BaseModel


class Role(EntityModel):
    """用户角色"""
    __tablename__ = 'auth_role'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_name = Column(String(48), comment='角色名称')
    cn_name = Column(String(40), comment='中文名称')
    is_active = Column(SmallInteger, comment='角色是否激活', default=1)

    # 多对多
    permissions = relationship('Permission', backref='roles', secondary='auth_role_permission')
    users = relationship('User', backref='roles', secondary='auth_user_role')


class Permission(EntityModel):
    """用户权限"""
    __tablename__ = 'auth_permission'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    permission_name = Column(String(64), comment='权限名称', unique=True)
    cn_name = Column(String(40), comment='权限中文名称', unique=True)


class User2Role(BaseModel):
    """用户角色中间表"""
    __tablename__ = 'auth_user_role'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_id = Column(BigInteger, ForeignKey('auth_role.id'), comment='角色外键')
    user_id = Column(BigInteger, ForeignKey('user.id'), comment='用户外键')


class Role2Permission(BaseModel):
    """角色权限中间表"""
    __tablename__ = 'auth_role_permission'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    role_id = Column(BigInteger, ForeignKey('auth_role.id'), comment='角色外键')
    permission_id = Column(BigInteger, ForeignKey('auth_permission.id'), comment='权限外键')
