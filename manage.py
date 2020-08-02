#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>


from app import init_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from flask import render_template, request, make_response, jsonify
from flask import redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
import os
from app.funlib import login_required, get_user_ip
from app.models import *
from flask import session

#blueprints;
from app.dashboard import dashboard as dashboard_blueprint
from app.sitesetting import sitesetting as setting_blueprint
from app.article import article as article_blueprint


envName = os.getenv('APP_ENV') or 'dev'
app = init_app( envName )

app.register_blueprint(dashboard_blueprint)
app.register_blueprint(setting_blueprint)
app.register_blueprint(article_blueprint)





# 开启CSRF防范功能
csrf =  CSRFProtect(app)

def make_shell_context():
    return dict(app=app, db=db)


# 初始化 migrate
# 两个参数一个是 Flask 的 app，一个是数据库 db

migrate = Migrate(app, db)


# 使用终端脚本工具启动和管理flask
manager = Manager(app)

# 添加 db 命令，并与 MigrateCommand 绑定
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(host='127.0.0.1', port=5050))


@app.route('/')
def app_index():
    if request.args.get('next'):
        session['next'] = request.args.get('next')
    return make_response(redirect('main'))

#500
@app.errorhandler(Exception)
def sever_error(e):
    app.logger.exception(e)
    if request.is_xhr:
        return make_response(jsonify({"code" : 1, "message" : "服务器端暂无法处理请求，请和管理员联系！"}))
    return render_template('500.html')

#404
@app.errorhandler(404)
def server_not_found(e):
    app.logger.exception(e)
    if request.is_xhr:
        return make_response(jsonify({"code" : 1, "message" : "[404]-服务器端暂无法处理请求，请和管理员联系！"}))
    return render_template('404.html')


#401
@app.errorhandler(401)
def server_not_found(e):
    app.logger.exception(e)
    if request.is_xhr:
        return make_response(jsonify({"code" : 1, "message" : "[401]-Unauthorized！"}))
    return render_template('401.html')


def get_tree_menu(pid=0, level=1):

    #最多支持三级，多了无效！
    if level == 1:
        pass
    elif level == 2:
        class_level = 'second'
    elif level == 3:
        class_level = 'third'
    else:
        class_level = 'unknown'

    tree_html = ''
    sql = '''
            select
                e.id,
                e.parentId,
                e.action,
                e.cname,
                e.icon
            from
                user as a left join user_role_map as b on a.username=b.user
                left join role as c on b.role=c.role
                left join role_module as d on c.role=d.role
                left join module as e on e.id = d.module
                where 1
                and a.valid='1'
                and b.valid='1'
                and c.valid='1'
                and e.valid='1'
                and e.parentId={}
                and a.username='{}'
                and e.level in (1,2,3)
                order by e.sq ASC
    '''.format(
        pid,
        session.get('username')
    )
    query = list( db.session.execute(sql) )
    if query:
        menu_list = []
        for q in query:
            if not q in menu_list:
                menu_list.append(q)

        for k, v in enumerate(menu_list):
            ul_start_html = ''
            ul_end_html = ''

            #非一级菜单，且只有一个子菜单
            if level > 1 and len(menu_list) == 1:
                ul_start_html = '<ul class="nav nav-{}-level collapse" aria-expanded="true" style="">'.format(class_level)
                ul_end_html = '''
                                </ul>
                            </li>
                '''
            #非一级菜单，且是第一个子菜单
            elif level > 1 and k==0:
                ul_start_html = '<ul class="nav nav-{}-level collapse" aria-expanded="true" style="">'.format(class_level)
                ul_end_html = ''

            #非一级菜单，且是最后一个子菜单
            elif level > 1 and k==(len(menu_list) -1):
                ul_start_html = ''
                ul_end_html = '''
                                </ul>
                            </li>    
                '''
            else:
                pass

            if level ==  1:
                #一级菜单，且只有一个选项；
                if v[2] != '#':
                    menu_html = '''
                        <li class="">
                            <a class="J_menuItem" href="{}"><i class="fa {}"></i>
                            <span class="nav-label">{}</span><span class="fa arrow"></span></a>
                    '''.format(v[2], v[4], v[3])
                else:
                    menu_html = '''
                        <li class="">
                            <a href="{}"><i class="fa {}"></i>
                            <span class="nav-label">{}</span><span class="fa arrow"></span></a>
                    '''.format( v[2], v[4], v[3])
            else:
                menu_html = '''
                    <li>
                        <a class="J_menuItem" href="{}" data-index="{}"><i class="fa {}"></i>{}</a>
                '''.format(v[2], v[0], v[4] or 'fa-toggle-right', v[3])

            tree_html += ul_start_html + menu_html + get_tree_menu(v[0], level+1) + ul_end_html
    elif level != 1:
        tree_html += "</li>"
    else:
        pass
    return tree_html



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

                #write history;
                login_ip = get_user_ip()
                login_history = LoginHistory(username=username, ip=login_ip)
                db.session.add(login_history)
                db.session.commit()

                #跳转
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
        query = list( db.session.execute(sql) )
        if not query:
            raise Exception("Error! user role unknown!")
        session['role'] = [ x[0] for x in query ]

    return render_template('index.html', menu=get_tree_menu())


if __name__ == '__main__':
    manager.run()
