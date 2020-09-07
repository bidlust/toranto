#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import Flask, session, request, make_response, flash, redirect, render_template, jsonify
from flask_session import Session
import os
from redis import StrictRedis
from flask_sqlalchemy import SQLAlchemy
from config import get_config
from flask_wtf.csrf import CSRFProtect
#配置数据库连接；
db = SQLAlchemy()

from .funlib import setup_log, get_user_ip, login_required, get_tree_menu
from .models import User, LoginHistory

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



@app.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():

    if session.get('auth'):
        return make_response(redirect('main'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('用户名或密码为空！')

        if username and password:
            current_user = User.query.filter_by(username=username).first()
            if current_user and current_user.check_password(password):
                session['auth'] = True
                session['username'] = username

                # write history;
                login_ip = get_user_ip()
                login_history = LoginHistory(username=username, ip=login_ip)
                db.session.add(login_history)
                db.session.commit()

                # 跳转
                resp = make_response(redirect('main'))
                return resp
            else:
                flash("用户名或密码错误！")

    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return make_response(redirect('login'))

@app.route('/main', methods=['GET'])
@login_required
def main_page():
    # query role
    if not session.get('role'):
        sql = '''
            select
                b.role
            from
                `user` AS a
            inner join user_role_map as b on a.username=b.user
            inner join role as c on b.role=c.role
            where 1
            and a.valid='1'
            and b.valid = '1'
            and c.valid = '1'
            and a.username = '{}'
        '''.format(
            session.get('username')
        )
        query = list(db.session.execute(sql))
        if not query:
            raise Exception("Error! user role unknown!")
        session['role'] = [ x[0] for x in query ]

    return render_template('index.html', menu=get_tree_menu())

@app.route('/')
def app_index():
    if request.args.get('next'):
        session['next'] = request.args.get('next')
    return make_response(redirect('main'))

#jinji2
@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt is None:
        fmt = '%Y-%m-%d %H:%M:%S'
    return date.strftime(fmt)

# 500
@app.errorhandler(Exception)
def sever_error(e):
    app.logger.exception(e)
    if request.is_xhr:
        return make_response(jsonify({"code": 1, "message": "服务器端暂无法处理请求，请和管理员联系！"}))
    return render_template('500.html')

# 404
@app.errorhandler(404)
def server_not_found(e):
    app.logger.exception(e)
    if request.is_xhr:
        return make_response(jsonify({"code": 1, "message": "[404]-服务器端暂无法处理请求，请和管理员联系！"}))
    return render_template('404.html')

# 401
@app.errorhandler(401)
def server_not_found(e):
    app.logger.exception(e)
    if request.is_xhr:
        return make_response(jsonify({"code": 1, "message": "[401]-Unauthorized！"}))
    return render_template('401.html')

