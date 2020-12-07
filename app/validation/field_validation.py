""" 
@Function:
@Author  : ybb
@Time    : 2020/9/28 18:11
"""
import math
import re
from datetime import datetime
from app.validation.exceptions import FieldValidException


class FieldValidation(object):

    def __init__(self, message=''):
        self.message = message

    def valid(self, val):
        raise ValueError('必须要定义valid方法')


class NotNull(FieldValidation):
    """字段必须传, 但可以为空"""

    def __init__(self, message='该字段必传'):
        super().__init__(message)

    def valid(self, val):
        if val is None:
            raise FieldValidException(self.message)
        return val


class NotEmpty(FieldValidation):
    """元素值不为null且不为空（字符串长度不为0、集合大小不为0）"""

    def __init__(self, message='该字段不能为空'):
        super().__init__(message)

    def valid(self, val):
        if not isinstance(val, bool):
            if not val:
                raise FieldValidException(self.message)
        return val


class AssertFalse(FieldValidation):
    """字段必须限制为False"""

    def __init__(self, message='该字段必须为False'):
        super().__init__(message)

    def valid(self, val):
        if isinstance(val, bool):
            if not val:
                return False
            raise FieldValidException(self.message)
        elif isinstance(val, int):
            if not val:
                return False
            raise FieldValidException(self.message)
        elif isinstance(val, str):
            if val == 'False' or val == 'false':
                return False
            raise FieldValidException(self.message)
        raise FieldValidException(self.message)


class AssertTrue(FieldValidation):
    """字段必须限制为True"""

    def __init__(self, message='该字段必须为True'):
        super().__init__(message)

    def valid(self, val):
        if isinstance(val, bool):
            if val:
                return True
            raise FieldValidException(self.message)
        elif isinstance(val, int):
            if val:
                return True
            raise FieldValidException(self.message)
        elif isinstance(val, str):
            if val == 'True' or val == 'true':
                return True
            raise FieldValidException(self.message)
        raise FieldValidException(self.message)


class DecimalMax(FieldValidation):
    """限制必须为一个不大于指定值的数字"""

    def __init__(self, num, message='该字段必须为一个不大于指定值的数字'):
        self.num = num
        super().__init__(message)

    def valid(self, val):
        if isinstance(val, (float, int)):
            if val > self.num:
                raise FieldValidException(self.message)
            else:
                return val
        raise FieldValidException('该字段必须是一个数字')


class DecimalMin(FieldValidation):
    """限制必须为一个不小于指定值的数字"""

    def __init__(self, num, message='该字段必须为一个不小于指定值的数字'):
        self.num = num
        super().__init__(message)

    def valid(self, val):
        if isinstance(val, (float, int)):
            if val < self.num:
                raise FieldValidException(self.message)
            else:
                return val
        raise FieldValidException('该字段必须是一个数字')


class Float(FieldValidation):
    """限制必须为一个小数"""

    def __init__(self, message='该字段必须必须为一个小数'):
        super().__init__(message)

    def valid(self, val):
        if not isinstance(val, float):
            raise FieldValidException(self.message)
        return val


class Digit(FieldValidation):
    """限制必须为数字类型, 整数或小数"""

    def __init__(self, message='该字段必须必须为一个数字'):
        super().__init__(message)

    def valid(self, val):
        if not isinstance(val, (float, int)):
            raise FieldValidException(self.message)
        return val


class Future(FieldValidation):
    """限制必须是一个将来的日期"""

    def __init__(self, message='该字段必须是一个将来的日期'):
        super().__init__(message)

    def valid(self, val):
        now = datetime.now()
        if not isinstance(val, datetime):
            if isinstance(val, str):
                try:
                    if ':' in val:
                        date = datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
                    elif '-' in val:
                        date = datetime.strptime(val, '%Y-%m-%d')
                    else:
                        timestamp = float(val)
                        date = datetime.fromtimestamp(timestamp)
                except (ValueError, TypeError):
                    raise FieldValidException(self.message)
            elif isinstance(val, (float, int)):
                date = datetime.fromtimestamp(val)
            else:
                raise FieldValidException(self.message)
        else:
            date = val
        if date is not None and date < now:
            raise FieldValidException(self.message)
        return date


class NotBlank(FieldValidation):
    """元素值不为空（不为null、去除首位空格后长度为0），
    不同于@NotEmpty，@NotBlank只应用于字符串且在比较时会去除字符串的空格"""

    def __init__(self, message='该字段不能为空'):
        super().__init__(message)

    def valid(self, val):
        if isinstance(val, str):
            val = val.strip()
        NotEmpty(self.message).valid(val)
        return val


class Email(FieldValidation):
    """元素值是Email，也可以通过正则表达式"""

    def __init__(self, message='该字段必须为email格式'):
        super().__init__(message)

    def valid(self, val):
        if isinstance(val, str) and re.match(r'^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', val):
            return val
        raise FieldValidException(self.message)


class Max(FieldValidation):
    """限制必须为数字且不大于指定值(整数)"""

    def __init__(self, max_, message=''):
        super().__init__(message)
        self.max_ = max_
        self.message = message or f'数字必须不大于{max_}'

    def valid(self, val) -> int:
        try:
            val = int(val)
        except (ValueError, TypeError):
            raise FieldValidException(self.message)
        if val > self.max_:
            raise FieldValidException(self.message)
        return val


class Min(FieldValidation):
    """限制必须为一个不小于指定值的数字(整数)"""

    def __init__(self, min_, message=''):
        super().__init__(message)
        self.min_ = min_
        self.message = message or f'数字必须不小于{min_}'

    def valid(self, val) -> int:
        try:
            val = int(val)
        except (ValueError, TypeError):
            raise FieldValidException(self.message)
        if val < self.min_:
            raise FieldValidException(self.message)
        return val


class Past(FieldValidation):
    """限制必须是一个过去的日期"""

    def __init__(self, message=''):
        super().__init__(message)

    def valid(self, val) -> datetime:
        """校验时间格式:
        可以是字符串形式的一串数字, 或者是数字 (时间戳)
        或者是 yyyy-mm-dd [HH:MM:SS]的格式
        """
        now = datetime.now()
        if not isinstance(val, datetime):
            if isinstance(val, str):
                try:
                    if ':' in val:
                        date = datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
                    elif '-' in val:
                        date = datetime.strptime(val, '%Y-%m-%d')
                    else:
                        timestamp = float(val)
                        date = datetime.fromtimestamp(timestamp)
                except (ValueError, TypeError):
                    raise FieldValidException(self.message)
            elif isinstance(val, (float, int)):
                date = datetime.fromtimestamp(val)
            else:
                raise FieldValidException(self.message)
        else:
            date = val
        if date is not None and date > now:
            raise FieldValidException(self.message)
        return date


class Pattern(FieldValidation):
    """限制必须符合指定的正则表达式"""

    def __init__(self, regex, message='该字段不能为空'):
        super().__init__(message)
        self.regex = regex

    def valid(self, val):
        if not re.match(self.regex, val):
            raise FieldValidException(self.message)
        return val


class Size(FieldValidation):
    """限制字符长度必须在min到max之间"""

    def __init__(self, min_=None, max_=None, message=''):
        assert min_ is not None or max_ is not None, '至少需要指定一个max或min'
        assert max_ is None or min_ <= max_, 'min必须不大于max'
        super().__init__(message)
        self.min_ = min_ or -math.inf
        self.max_ = max_ or math.inf
        self.message = message
        if message == '':
            if min_ is None:
                self.message = f'必须是字符串且长度必须不大于{self.max_}'
            elif max_ is None:
                self.message = f'必须是字符串且长度必须不小于{self.min_}'
            else:
                self.message = f'必须是字符串且长度必须在{self.min_}到{self.max_}之间'

    def valid(self, val):
        if isinstance(val, str) and self.min_ <= len(val) <= self.max_:
            return val
        raise FieldValidException(self.message)


class NumRange(FieldValidation):
    """限定传入的必须是自然数，且在指定的范围内"""
    message: str

    def __init__(self, min_: int, max_: int, message=''):
        super().__init__(message)
        self.min_ = min_
        self.max_ = max_
        self.message = message
        if message == '':
            if not isinstance(self.min_, int):
                assert f'{self.min_}必须是一个int类型的自然数'
            elif not isinstance(self.max_, int):
                assert f'{self.max_}必须是一个int类型的自然数'

    def valid(self, val) -> int:
        if not isinstance(val, int):
            self.message = '该字段必须是一个int类型的自然数'
            raise FieldValidException(self.message)
        if self.min_ <= val <= self.max_:
            return val
        self.message = f'该字段必须是一个介于{self.min_}和{self.max_}之间的自然数'
        raise FieldValidException(self.message)


class DatetimeFormat(FieldValidException):
    """传入的日期时间格式必须符合规定"""

    def __init__(self, message='该字段必须是一个日期时间格式'):
        super().__init__(message)

    def valid(self, val):
        if isinstance(val, datetime):
            return val
        if not isinstance(val, str):
            raise FieldValidException('该字段必须是一个字符串格式')
        try:
            if ':' in val:
                date = datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
            elif '-' in val:
                date = datetime.strptime(val, '%Y-%m-%d')
            else:
                raise FieldValidException(self.message)
        except (ValueError, TypeError):
            raise FieldValidException(self.message)
        return date


class IsPhone(FieldValidException):
    """传入字符串是否是正确的手机号"""

    def __init__(self, message='该字段必须是一个字符串格式'):
        super().__init__(message)

    def valid(self, val):
        if not isinstance(val, str):
            raise FieldValidException('该字段必须是一个字符串格式')
        code = re.match(r'^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0-3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$', val)
        if not code:
            raise FieldValidException('手机号码格式不正确')
        return val

