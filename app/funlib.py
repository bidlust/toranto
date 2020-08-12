#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>


import logging
from logging.handlers import TimedRotatingFileHandler
import pickle
from hashlib import md5
import os
import datetime
import calendar
from flask import current_app as app
from flask import session, request, make_response, jsonify, redirect
import cx_Oracle
import functools


# 把日志相关的配置封装成一个日志初始化函数
def setup_log(Config):
    # 设置日志的记录等级
    logging.basicConfig(level=Config.LOG_LEVEL)  # 调试debug级
    file_log_handler = TimedRotatingFileHandler( Config.LOG_PATH,
    # 按天切分；
    when="D",
    # 每天都切分。 比如interval=2就表示两天切分一下。
    interval=1,
    # 保留15天的日志
    backupCount=15,
    # 使用UTF-8的编码来写日志
    encoding="UTF-8",
    delay=False,
    # 使用UTC+0的时间来记录 （一般docker镜像默认也是UTC+0）
    utc=True

    )

    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flaskapp使用的）添加日志记录器
    logging.getLogger().addHandler( file_log_handler )


def raise_exception(msg):
    raise Exception(msg)

#获取随机数；
def get_random(random_length=32):
    return md5(os.urandom( random_length )).hexdigest()

#生成日期列表
def create_assist_date(**kwargs):

    date_start = kwargs.get('date_start')
    date_end = kwargs.get('date_end')
    if not date_start or not date_end:
        raise_exception("[Error] - function: create_assist_date [Message] params empty!")

    date_start = datetime.datetime.strptime(date_start, "%Y-%m-%d")
    date_end = datetime.datetime.strptime(date_end, "%Y-%m-%d")
    date_list = []
    date_list.append( date_start.strftime("%Y-%m-%d"))
    while date_start < date_end:
        date_start += datetime.timedelta(days=+1)
        date_list.append(date_start.strftime("%Y-%m-%d"))
    return date_list

#获取指定年、月的第一天和最后一天
def get_date_range(year, month):
    if year > 0 and month>0:
        week, monthRange = calendar.monthrange(year, month)
        return datetime.date(year=year, month=month, day=1), \
        datetime.date(year=year, month=month, day=monthRange)

def get_db_config(sqlType):

    if sqlType == 'Mysql':

        config = {
            'host' : app.config.get('MYSQL_HOST'),
            'port' : app.config.get('MYSQL_PORT'),
            'user' : app.config.get('MYSQL_USER'),
            'password' : app.config.get('MYSQL_PWD'),
            'database' : app.config.get('MYSQL_DBNAME'),
            'charset' : app.config.get('MYSQL_CHARSET'),
            'cusorclass' :  app.config.get('MYSQL_CURSOR')
        }
    elif sqlType == 'Oracle':

        config = {
            'host' : app.config.get('ORACLE_HOST'),
            'port' :  app.config.get('ORACLE_PORT'),
            'user' : app.config.get('ORACLE_USER'),
            'password' : app.config.get('ORACLE_PWD'),
            'sid' : app.config.get('ORACLE_SID'),
        }
    else:
        config = {

        }

    return config

def oracle_fetch_one(sql):

    oracle_config = get_db_config('Oracle')
    try:
        dsn_tns = cx_Oracle.makedsn(oracle_config.get('host'),oracle_config.get('port'),oracle_config.get('sid') )
        oracle_conn = cx_Oracle.connect( oracle_config.get('user'),oracle_config.get('password'), dsn_tns)
        oracle_cursor = oracle_conn.cursor()
        _rtf = oracle_cursor.execute( sql )
        return _rtf.fetchone() or None
    except Exception as e:
        raise
    finally:
        oracle_cursor.close()
        oracle_conn.close()

def oracle_fetch_many(sql):

    oracle_config = get_db_config('Oracle')
    try:
        dsn_tns = cx_Oracle.makedsn(oracle_config.get('host'),oracle_config.get('port'),oracle_config.get('sid') )
        oracle_conn = cx_Oracle.connect( oracle_config.get('user'),oracle_config.get('password'), dsn_tns)
        oracle_cursor = oracle_conn.cursor()
        _rtf = oracle_cursor.execute( sql )
        return _rtf.fetchmany() or None
    except Exception as e:
        raise
    finally:
        oracle_cursor.close()
        oracle_conn.close()

def oracle_fetch_all(sql):

    oracle_config = get_db_config('Oracle')
    try:
        dsn_tns = cx_Oracle.makedsn(oracle_config.get('host'),oracle_config.get('port'),oracle_config.get('sid') )
        oracle_conn = cx_Oracle.connect( oracle_config.get('user'),oracle_config.get('password'), dsn_tns)
        oracle_cursor = oracle_conn.cursor()
        _rtf = oracle_cursor.execute( sql )
        return _rtf.fetchall() or None
    except Exception as e:
        raise
    finally:
        oracle_cursor.close()
        oracle_conn.close()



def login_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        if not session.get('auth'):
            if request.is_xhr:
                return make_response(jsonify({"code" :1 , "message":"[Waring] login timeout!"}))
            return redirect("/login")
        return func(*args, **kwargs)
    return decorator


def get_user_ip():
    client_ip = '127.0.0.1'
    try:
        client_ip = request.environ.get['HTTP_X_REAL_IP']
    except Exception:
        client_ip = request.headers.get('X-Forwarded-For')
    except Exception:
        client_ip = request.remote_addr

    return client_ip


def zip_dict(title, contents):
    if not isinstance(title, list):
        raise Exception("[Error] - title must be list!")
    if not isinstance(contents, list):
        raise Exception("[Error] - content must be list!")
    zipped_list = []
    for content in contents:
        if len(title) != len(content):
            return Exception("[Error] - title and content length not equals!")
        zipped_list.append( { k:v for (k,v) in zip(title, content) } )
    return zipped_list
