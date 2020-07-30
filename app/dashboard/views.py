#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import render_template

from . import dashboard



@dashboard.route('/dashboard_index/', methods=['POST', 'GET'])
def dashboard_index():

    return render_template('dashboard_index.html')
