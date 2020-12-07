# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    test_cache
   Author：       yscl
   date：         2020/12/7 10:50:15
   Description：  
  
-------------------------------------------------
"""

from app import create_app

cur_app = create_app()
ctx = cur_app.app_context()
ctx.push()


def test_cache():
    with cur_app.test_client() as c:
        from app.commons.cache.cache import BaseCache
        BaseCache.set_with_pickle('t1', 'abc')
        t1 = BaseCache.get_with_pickle('t1')
        print(t1)
        BaseCache.prefix_client().set("test1", "666")
        print(BaseCache.prefix_client().get("test1"))
        BaseCache.set_with_pickle("t2", {1, 2, 3, 4, 5})
        print(BaseCache.get_with_pickle('t2'))
        BaseCache.prefix_client().mset({'a': '2', 'b': '3', 'c': 4})
        print(BaseCache.prefix_client().mget(['a', 'b', 'c']))
        print(BaseCache.prefix_client().mget('a'))


test_cache()
