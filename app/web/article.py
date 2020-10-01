#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import render_template, request, session, abort
from app.models import Article, Category, Link
from app import db, app
from . import web
import datetime
from sqlalchemy.sql import func

@web.route('/article/<string:seo>', methods=['GET', 'POST'])
def web_article(seo):
    params = list()
    params.append(Article.isvisible == 1)
    params.append(Article.ispublish == 1)
    params.append(Article.valid == 1)
    params.append(Article.deleted_at == None )
    params.append(Article.date_expire > datetime.datetime.now().strftime("%Y-%m-%d"))
    params.append(Article.article_seo == seo)

    article = db.session.query(Article).filter(*params).first()

    # category
    category = db.session.query(
        Category.category_name,
        Category.category_desc
    ).filter(Category.deleted_at == None, Category.valid == '1').all()

    # tags
    tags = db.session.query(
        Article.article_tag
    ).filter(Article.deleted_at == None, Article.ispublish == 1, Article.isvisible == 1, Article.valid == 1).all()

    tag_set = set()
    for tag in tags:
        tag_set.update([g for g in tag[0].split("@") if g])

    # 友情链接
    link = db.session.query(
        Link.link_name,
        Link.link_href,
        Link.link_desc
    ).filter(Link.deleted_at == None, Link.valid == 1).all()

    # archive by date
    archives = db.session.query(
        func.date_format(Article.created_at, "%Y-%m"), func.count('*').label('t')
    ).filter(*params).group_by(func.date_format(Article.created_at, "%Y-%m")).all()

    if article:
        return render_template(
            '{}/article.html'.format(session.get('skin')),
            setting=session.get('setting'),
            article=article,
            category=category,
            link=link,
            archives=archives,
            tag_set=tag_set
        )
    else:
        abort(404)


