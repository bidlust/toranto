#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import render_template, request


from . import web


@web.route('/index', methods=['GET', 'POST'])
def web_index():

    try:
        page= int( request.args.get('page') )
    except Exception :
        page = 1



    return render_template('index.html')