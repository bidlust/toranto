#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from app import app,db, csrf
from flask import  session, request, make_response, flash, redirect, render_template, jsonify
from .funlib import  get_user_ip, login_required, get_tree_menu, get_random
from .models import User, LoginHistory, TorantoSetting
from sqlalchemy import desc

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

    return render_template('main.html', menu=get_tree_menu())

@app.route('/')
def app_index():
    #setting = db.session.query(TorantoSetting).order_by(desc(TorantoSetting.created_at)).first()

    setting = TorantoSetting.query.order_by(desc(TorantoSetting.created_at)).first()

    return make_response(render_template('index.html', setting=setting, random=get_random()))


@app.route('/admin')
def app_admin():
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


