#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import Flask
from flask_session import Session
from redis import StrictRedis
from flask_sqlalchemy import SQLAlchemy
from .funlib import setup_log
from config import get_config

#配置数据库连接；
db = SQLAlchemy()


def init_app(cfg):

    app = Flask(__name__, static_url_path='/static',static_folder='static', template_folder='templates')

    # 设置配置类
    Config = get_config( cfg )
    # 加载配置
    app.config.from_object(Config)

    setup_log(Config)

    # redis的链接初始化
    #     global redis_store
    #     redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT,db=0)

    # 开启session功能
    Session(app)

    # 配置数据库链接
    db.init_app(app)

    # TODO 注册蓝图对象到app应用中


    return app
