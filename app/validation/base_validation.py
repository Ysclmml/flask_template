""" 
@Function:
@Author  : ybb
@Time    : 2020/9/28 18:12
"""
from typing import Dict
from flask import request

from app.validation.exceptions import ValidException, FieldValidException
from app.validation.field_validation import FieldValidation


class BaseValidation(object):
    """用户创建需要校验的字段"""

    def __init__(self, _cls):
        self._cls = _cls

    def __call__(self, func, *args, **kw):
        def wrapper(*args, **kw):
            self.valid_data()
            return func(*args, **kw)
        return wrapper

    def valid_data(self) -> 'BaseValidation':
        """
        :param {dict} data:
        :param {dict} rules:
        :return: {BaseValidation}
        """
        rules: Dict = {}
        for attr, value in self._cls.__dict__.items():
            if isinstance(value, list):
                rules.setdefault(attr, value)
        return type('__Validation', (BaseValidation,), {'valid_rules': rules})(self._cls)._valid()

    def _valid(self):
        errors = {}
        validated_data = {}
        data = request.get_json(silent=True)
        # Single field verification
        for field, rules in self.valid_rules.items():
            # 不存在字段就不走校验
            val = data.get(field, None)
            if isinstance(val, type(None)):
                continue
            field_errors = []
            ret_val = None
            for rule in rules:  # type: FieldValidation
                try:
                    ret_val = rule.valid(val)
                except FieldValidException as e:
                    field_errors.append(e.message)
            if not field_errors:
                validated_data[field] = ret_val
                continue
            errors[field] = field_errors
        # global validates
        if hasattr(self._cls, 'validate'):
            data = getattr(self._cls, 'validate')(self, data)
            if data:
                request.get_json(silent=True).update(data)
        if errors:
            raise ValidException(message=errors)
        self.validated_data = validated_data

    def valid_rules(self):
        """校验规则, 返回字典, [列表是一个校验器]
        return {
            'username': [NotNull(message=""), Min(2)],
            'password': [],
            'phone': [],
            'display': [],
        }
        """
        raise ValueError('必须定义校验规则')
