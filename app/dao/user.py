# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    user
   Author：       yscl
   date：         2020/12/3 15:50:51
   Description：  
  
-------------------------------------------------
"""
from app.models.user import User, Info, Group


class UserDao(object):

    @staticmethod
    def get_first() -> User:
        # user = User.query.filter(User.id == 1)
        user = User.query.all()
        user = list(user)
        print(user)
        return user

    @staticmethod
    def create_user():
        User.create(name="测试测试")

    @staticmethod
    def relation_test():
        user = User.query.filter_by(id=1).first()
        # print(list(user.info))
        info = Info.query.join(User).filter(User.id == 1)
        Info.query.filter
        group = Group.query.filter(Group.id == 1).first()
        print('tttt', group.user)
        print(list(info))
        return user


