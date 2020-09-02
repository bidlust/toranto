#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>


from flask import make_response, render_template, jsonify, request, flash, session
from . import article
from app.models import TorantoSetting
from app import db
from app.models import Article
from flask import current_app as app
import datetime
from app.funlib import *
from sqlalchemy.sql import func


@article.route('/lists/', methods=['POST', 'GET'])
def article_lists():

    if request.method == 'POST':
        try:
            pageSize    =    int( request.form.get('pageSize') )
            pageNumber  =    int( request.form.get('pageNumber') )
        except Exception:
            pageSize =  app.config.get('PAGE_SIZE')
            pageNumber = 1

        params = []
        params.append(Article.isvisible == '1')
        params.append(Article.ispublish == '1')
        params.append(Article.valid == '1')
        params.append(db.cast( Article.date_expire, db.Date) > db.cast(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), db.Date))

        article_title = request.form.get('article_title')
        if article_title:
            params.append(Article.article_title==article_title)
        if not 'root' in session.get('role'):
            params.append(Article.article_author==session.get('username'))

        
        pagination = db.session.query(
            Article.article_title,
            func.date_format( Article.created_at, "%Y-%m-%d %H:%m:%S"),
            Article.article_author,
            Article.article_click,
            Article.top,
            Article.iscomment,
            Article.ispublish,
            Article.isvisible,
            Article.article_password
        ).filter(*params)\
            .order_by(Article.top.desc(), Article.sq.desc())\
            .paginate(pageNumber, per_page=pageSize, error_out=True)

        total = pagination.total
        items = pagination.items
        title = ['title', 'created', 'author', 'click', 'top', 'iscomment', 'ispublish', 'isvisible', 'ispassword' ]
        return make_response(jsonify({"code" : 0, "rows": zip_dict(title, list( items ) ) , "total":total}))

    return render_template('article.html')


@article.route('/create/', methods=['POST', 'GET'])
def article_create():

    return render_template('article_create.html')
