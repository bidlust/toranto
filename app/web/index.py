#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import render_template, request
from app.models import Article
from app import db, app
from . import web
import datetime

@web.route('/index', methods=['GET', 'POST'])
def web_index():

    try:
        page_number = int( request.args.get('page') )
    except Exception :
        page_number = 1

    #article
    params = list()
    params.append(Article.isvisible == 1)
    params.append(Article.ispublish == 1)
    params.append(Article.date_expire > datetime.datetime.now().strftime("%Y-%m-%d"))

    page_size = app.config.get('PAGE_SIZE')

    pagination = db.session.query(
        Article.article_click,
        Article.article_desc,
        Article.article_title,
        Article.article_author,
        Article.article_category,
        Article.article_tag

    ).filter(*params).order_by(Article.top.desc(), Article.created_at.desc(), ) \
    .paginate(page_number, per_page=page_size, error_out=True)
    total_number = pagination.total
    articles = pagination.items
    return render_template('index.html', articles=articles, totalNum=total_number)
