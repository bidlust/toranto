#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>


from app import init_app
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
import os
from app.models import *

envName = os.getenv('APP_ENV') or 'dev'
app = init_app( envName )


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



if __name__ == '__main__':
    manager.run()
