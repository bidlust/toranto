#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import Flask
from flask_session import Session
import os
from redis import StrictRedis
from flask_sqlalchemy import SQLAlchemy
from config import get_config
from flask_wtf.csrf import CSRFProtect
#配置数据库连接；
db = SQLAlchemy()

from .funlib import setup_log

app = Flask(__name__, static_url_path='/static',static_folder='static', template_folder='templates')

# 设置配置类
envName = os.getenv('APP_ENV') or 'dev'
Config = get_config( envName )
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

# 开启CSRF防范功能
csrf = CSRFProtect(app)

# TODO 注册蓝图对象到app应用中
#blueprints;
from app.dashboard import dashboard as dashboard_blueprint
from app.sitesetting import sitesetting as setting_blueprint
from app.article import article as article_blueprint
from app.category import category as category_blueprint
from app.link import link as link_blueprint
from app.action import action as action_blueprint

app.register_blueprint(dashboard_blueprint)
app.register_blueprint(setting_blueprint)
app.register_blueprint(article_blueprint)
app.register_blueprint(category_blueprint)
app.register_blueprint(link_blueprint)
app.register_blueprint(action_blueprint)

from . import views

