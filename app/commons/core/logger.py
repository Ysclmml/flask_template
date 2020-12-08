# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    logger
   Author：       yscl
   date：         2020/12/2 14:35:52
   Description：  
  
-------------------------------------------------
"""
import json
import os
import time
from datetime import datetime
from logging.config import dictConfig

from flask import g, request, _request_ctx_stack


def logging_config():
    # logging日志配置
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    logger_path = os.path.join(os.path.dirname(base_dir), 'logs')
    logger_file = '{}_logs.log'.format(datetime.today().strftime('%Y-%m-%d'))
    os.makedirs(logger_path, exist_ok=True)
    full_logger_path = os.path.join(logger_path, logger_file)
    logger_dict = {
        'version': 1,  # 该配置写法固定
        'formatters': {  # 设置输出格式
            'default': {
                'format': "[%(levelname)s] - %(asctime)s - %(name)s - : %(message)s in %(pathname)s:%(lineno)d", }
        },
        # 设置处理器
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                # 'stream': 'ext://sys.stdout',
                'formatter': 'default',
                'level': 'INFO'
            },
            # 输出日志到文件，按日期滚动
            'file': {
                'level': 'INFO',
                'class': 'logging.handlers.TimedRotatingFileHandler',
                # TimedRotatingFileHandler的参数
                # 参照https://docs.python.org/3/library/logging.handlers.html#timedrotatingfilehandler
                # 目前设定每天一个日志文件
                'filename': full_logger_path,
                'when': 'midnight',
                'interval': 1,
                'backupCount': 10,
                'formatter': 'default'
            },
        },
        # 设置root日志对象配置
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
        # 设置其他日志对象配置
        'loggers': {
            'test': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': 0
            },
            'flask': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': 0
            }
        }
    }
    dictConfig(logger_dict)


# 记录每次请求的性能
def apply_request_log(app):
    @app.before_request
    def request_cost_time():
        g.request_start_time = time.time()
        g.request_time = lambda: "%.5f" % (time.time() - g.request_start_time)

    @app.after_request
    def log_response(res):
        message = '[%s] -> [%s] from:%s costs:%.3f ms' % (
            request.method,
            request.path,
            request.remote_addr,
            float(g.request_time()) * 1000
        )
        req_body = request.get_json() if request.get_json() else {}
        data = {
            'path': _request_ctx_stack.top.request.view_args,
            'query': request.args,
            'body': req_body
        }
        message += '\n\"data\": ' + json.dumps(data, indent=4, ensure_ascii=False)
        # 设置颜色开始(至多3类参数，以m结束)：\033[显示方式;前景色;背景色m
        print('\033[0;34m')
        if request.method in ('GET', 'POST', 'PUT', 'DELETE'):
            print(message)
        print('\033[0m')  # 终端颜色恢复
        return res


# 基于ip解析真实地址
def parse_location_by_ip(ip: str):
    """
    :param ip: ip地址
    :return: ip所在的省市
    """
    if ip == '127.0.0.1' or ip.startswith('192.168.'):
        return "内网IP"
    from app.libs.httper import HTTP
    try:
        url = 'http://whois.pconline.com.cn/ipJson.jsp?{0}&json=true'.format(ip)
        json_data = HTTP.get(url)
        return '{0} {1}'.format(json_data['pro'], json_data['city'])
    except Exception:
        return '获取地理位置异常 {ip}'.format(ip=ip)
