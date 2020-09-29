#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import render_template, request, session
from app.models import Article, TorantoSetting, Navigate, Category, Link
from app import db, app
from . import web
import datetime
from sqlalchemy import func
from app.classes.Page import Page

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
    params.append(Article.valid == 1)
    params.append(Article.date_expire > datetime.datetime.now().strftime("%Y-%m-%d"))

    page_size = app.config.get('PAGE_SIZE')

    pagination = db.session.query(
        Article.article_click,
        Article.article_desc,
        Article.article_title,
        Article.article_author,
        Article.article_category,
        Article.article_tag,
        Article.article_seo,
        Article.updated_at
    ).filter(*params).order_by(Article.top.desc(), Article.created_at.desc(), ) \
    .paginate(page_number, per_page=page_size, error_out=True)
    total_number = pagination.total
    articles = pagination.items
    #navigate
    navigate = db.session.query(
        Navigate.navigate_name,
        Navigate.navigate_tag,
        Navigate.navigate_icon,
        Navigate.navigate_url
    ).filter(Navigate.deleted_at == None).order_by(Navigate.sq.asc()).all()

    #tags
    tags = db.session.query(
        Article.article_tag
    ).filter(Article.deleted_at == None, Article.ispublish==1, Article.isvisible==1, Article.valid==1).all()

    tag_set = set()
    for tag in tags:
        tag_set.update( [ g for g in tag[0].split("@") if g  ] )

    #article total
    articleCount = db.session.query(
        Article.article_tag
    ).filter(*params).count()

    #visit total
    clickCount = db.session.query(
        func.sum( Article.article_click )
    ).filter(*params).scalar()

    #archive by date
    archives = db.session.query(
        func.date_format( Article.created_at , "%Y-%m"), func.count('*').label('t')
    ).filter(*params).group_by( func.date_format( Article.created_at , "%Y-%m") ).all()
    #footer

    #category
    category = db.session.query(
        Category.category_name,
        Category.category_desc
    ).filter(Category.deleted_at==None, Category.valid=='1').all()

    #友情链接
    link = db.session.query(
        Link.link_name,
        Link.link_href,
        Link.link_desc
    ).filter(Link.deleted_at==None, Link.valid==1).all()
    #页脚-分页
    obj = Page(page_number, total_number, "/article/", page_size, 10 )  # 把数据传进去
    page_html = obj.page_html()

    return render_template(
                            '{}/index.html'.format(session.get('skin')),
                            articles=articles,
                            setting=session.get('setting'),
                            navigate=navigate,
                            tag_set=tag_set,
                            articleCount=articleCount,
                            clickCount=clickCount,
                            archives=archives,
                            page_html=page_html,
                            category=category,
                            link=link
                           )
