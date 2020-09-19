#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import render_template, request, session
from app.models import Article, TorantoSetting, Navigate
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

    #settings
    site_setting = db.session.query(TorantoSetting.key, TorantoSetting.value).filter(TorantoSetting.valid=='1').all()
    setting = {k:v for (k, v) in site_setting}

    #navigate
    navigate = db.session.query(
        Navigate.navigate_name,
        Navigate.navigate_tag,
        Navigate.navigate_url
    ).filter(Navigate.deleted_at == None).order_by(Navigate.sq.asc()).all()

    #article
    articles = db.session.query(
        Article.article_tag,
        Article.article_category,
        Article.article_author,
        Article.article_click,
        Article.article_desc,
        Article.created_at
    ).filter(Article.deleted_at==None, Article.ispublish=='1', Article.valid=='1') \
    .order_by(Article.top.desc(), Article.created_at.desc()).all()

    return render_template('{}/index.html'.format(session.get('skin')),
                           articles=articles,
                           totalNum=total_number,
                           setting=setting,
                           navigate=navigate,
                           )
