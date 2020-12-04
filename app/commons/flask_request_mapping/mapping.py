""" 
@Function:
@Author  : ybb
@Time    : 2020/10/10 8:57
"""
import inspect
import logging
from functools import partial

from flask.views import View


logger = logging.getLogger('request_mapping.mapping')


# copy django.utils.decorations
class classonlymethod(classmethod):
    def __get__(self, instance, cls=None):
        if instance is not None:
            raise AttributeError("This method is available only on the class, not on instances.")
        return super(classonlymethod, self).__get__(instance, cls)


@classonlymethod
def as_view(cls, actions,  *class_args, **class_kwargs):
    """Converts the class into an actual view function that can be used
    with the routing system.  Internally this generates a function on the
    fly which will instantiate the :class:`View` on each request and call
    the :meth:`dispatch_request` method on it.

    The arguments passed to :meth:`as_view` are forwarded to the
    constructor of the class.
    """

    def view(*args, **kwargs):
        self = view.view_class(*class_args, **class_kwargs)

        for method, (action, _) in actions.items():
            handler = getattr(self, action)
            setattr(self, method, handler)

        if hasattr(self, 'get') and not hasattr(self, 'head'):
            self.head = self.get
        return self.dispatch_request(*args, **kwargs)

    if cls.decorators:
        # view.__name__ = name
        view.__module__ = cls.__module__
        for decorator in cls.decorators:
            view = decorator(view)

    # We attach the view class to the view function for two reasons:
    # first of all it allows us to easily figure out what class-based
    # view this thing came from, secondly it's also used for instantiating
    # the view class so you can actually replace it with something else
    # for testing purposes and debugging.
    view.view_class = cls
    # view.__name__ = name
    view.__doc__ = cls.__doc__
    view.__module__ = cls.__module__
    view.methods = cls.methods
    view.provide_automatic_options = cls.provide_automatic_options
    return view


class RequestMapping(object):
    def __init__(self, value: str, method: str, **kwargs):
        """

        :param value: 路由地址
        :param method: 路由方法
        :param kwargs: 额外的参数传给flask路由
        """
        self.value: str = value
        self.method: str = method
        self.kwargs: dict = kwargs


def request_mapping(value: str, method: str = 'get', **kwargs):
    """
    :param value: The path mapping URIs (e.g. "/myPath.do")
    :param method:  The HTTP request methods to map to, narrowing the primary mapping:
     get, post, head, options, put, patch, delete, trace
    """

    def get_func(o: type(View), v: str):
        setattr(o, 'request_mapping', RequestMapping(v, method, **kwargs))
        if inspect.isclass(o):
            if not value.startswith('/'):
                logger.warning("values should startswith / ")
            o.as_view = as_view
        return o

    return partial(get_func, v=value)


