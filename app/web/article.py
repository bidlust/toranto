#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import render_template, request, session, abort
from app.models import Article, TorantoSetting, Navigate
from app import db, app
from . import web
import datetime


@web.route('/article/<string:seo>', methods=['GET', 'POST'])
def web_article(seo):

    article = db.session.query(Article).filter(Article.article_seo==seo, Article.ispublish=='1', Article.isvisible=='1', Article.deleted_at==None).first()
    if article:
        return render_template('{}/article.html'.format(session.get('skin')),  setting=session.get('setting'),  article=article)
    else:
        abort(404)

