# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    user
   Author：       yscl
   date：         2020/12/3 15:50:51
   Description：  
  
-------------------------------------------------
"""
from app.models.user import User, Info, Group, Group2User


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

        group = Group.query.filter(Group.id == 1).first()
        print('tttt', group.user)
        print(list(info))
        group2 = Group.query.with_entities(Group.id, Group.groupname).join(Group2User).filter(Group2User.user_id == 1)
        print('部分字段1', group2, type(group2), list(group2))
        group2 = Group.query.join(Group2User).filter(Group2User.user_id == 1)
        print('部分字段2', group2, type(group2), list(group2))
        print(Group.query.join(Group2User).filter(Group2User.user_id == 1).values_list('groupname', 'id'))
        print(Group.query.join(Group2User).filter(Group2User.user_id == 1).values_list('groupname', flat=True))
        print(Group.query.join(Group2User).filter(Group2User.user_id == 1).values_dict('groupname'))
        print(Group.query.join(Group2User).filter(Group2User.user_id == 1).values_dict('groupname', 'id'))
        print(Group.query.join(Group2User).with_entities(Group.id, Group.groupname).filter(Group2User.user_id == 1).values_dict('id', 'groupname'))
        print(Group.query.join(Group2User).with_entities(Group.id, Group.groupname).filter(Group2User.user_id == 1).values_list('id', flat=True))
        print(Group.query.join(Group2User).with_entities(Group.id, Group.groupname).filter(Group2User.user_id == 1).values_list('id'))
        return user
