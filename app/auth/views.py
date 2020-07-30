#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import render_template
from . import auth


@auth.route('/login', methods=['GET','POST'])
def auth_login():

    return render_template('login.html')
