#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>


from flask import make_response, render_template, jsonify, request, flash, session

from . import article
from app.models import TorantoSetting
from app import db



@article.route('/lists/', methods=['POST', 'GET'])
def article_lists():


    return render_template('article.html')