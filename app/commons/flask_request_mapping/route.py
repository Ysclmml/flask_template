""" 
@Function:
@Author  : ybb
@Time    : 2020/10/10 9:08
"""
from typing import Dict, Tuple

from flask import Flask

from .mapping import RequestMapping


def _fix_path_value(full_value: str) -> str:
    # 移除多余的斜杠
    full_value = full_value.replace('//', '/', 1)
    return full_value


def update_url_map(app: Flask, clazz, url_patterns_dict):
    for full_value, actions in url_patterns_dict.items():
        # 如果不指定endpoint, 默认使用类名+函数名作为end_point
        view_func = clazz.as_view(actions)
        for method, (func_name, kwargs) in actions.items():
            endpoint = kwargs.pop('endpoint', None)
            if endpoint is None:
                endpoint = '{}_{}'.format(clazz.__name__.lower(), func_name.lower())
            app.add_url_rule(full_value, view_func=view_func, methods=[method], endpoint=endpoint, **kwargs)


def register(app: Flask, clazz):
    """注册路由"""
    class_request_mapping: RequestMapping = getattr(clazz, 'request_mapping', None)
    if class_request_mapping is None:
        raise RuntimeError('view class should use request_mapping decorator.')

    # path value on class decorator
    class_path_value = class_request_mapping.value

    url_patterns_dict: Dict[str, Dict] = dict()
    for func_name in dir(clazz):
        func = getattr(clazz, func_name)
        mapping: RequestMapping = getattr(func, 'request_mapping', None)
        if mapping is None:
            continue
        request_method = mapping.method
        # path value on method decorator
        method_path_value = mapping.value
        method_kwargs = mapping.kwargs
        # 拼接类上的路径与方法上的路径
        full_value = class_path_value + method_path_value
        full_value = _fix_path_value(full_value)

        if full_value in url_patterns_dict:
            temp_func_name, _ = url_patterns_dict[full_value].setdefault(request_method, (func_name, method_kwargs))
            # check if method and path are duplicated
            assert temp_func_name == func_name, "path: {} with method: {} is duplicated".format(
                full_value,
                request_method
            )
        else:
            url_patterns_dict[full_value] = {request_method: (func_name, method_kwargs)}

    # 添加到flask的app上
    update_url_map(app, clazz, url_patterns_dict)
