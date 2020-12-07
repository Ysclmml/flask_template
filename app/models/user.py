# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    user
   Author：       yscl
   date：         2020/12/3 15:46:50
   Description：  
  
-------------------------------------------------
"""
from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship

from app.commons.core.db import EntityModel, BaseModel


class User(EntityModel):
    """用户model对象"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(24), comment='昵称')

    # info = relationship('Info', lazy='dynamic', backref='user')  # 一对多, 返回是一个列表
    info = relationship('Info', backref='user', uselist=False)  # 一对一, 返回直接是关联对象, 此外不能使用dynamic, 在`一中`的关系

    def __repr__(self):
        return '<User(id={0}, name={1})>'.format(self.id, self.name)

    def keys(self):
        self.append('name')
        return self.fields


class Info(EntityModel):
    """用户详情"""
    __tablename__ = 'info'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    province = Column(String(24), comment='省份')
    city = Column(String(24), comment='城市')

    user_id = Column(Integer, ForeignKey('user.id'), comment='用户外键')


class Group(BaseModel):
    __tablename__ = 'groups'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    groupname = Column(String(24), comment='分组名称')
    user = relationship('User', backref='group', secondary='group_user')


class Group2User(BaseModel):
    __tablename__ = 'group_user'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('user.id'), comment='外键')
    group_id = Column(BigInteger, ForeignKey('groups.id'), comment='外键')
