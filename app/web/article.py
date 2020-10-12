#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import render_template, request, session, abort, make_response, jsonify
from app.models import Article, Category, Link, Comment
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


@web.route('/comment', methods=['GET', 'POST'])
def web_comment():

    username = request.form.get('username')
    email = request.form.get('email')
    url = request.form.get('url')
    content = request.form.get('comment_message')
    cparent = request.form.get('cparent') or 0
    article_id = request.form.get('article_id')
    comment_type = request.form.get('ctype') or 'article'
    comment_article_title = request.form.get('article_title')

    if not comment_article_title:
        return make_response(jsonify({"code": 1, "message": "[err01] - 对不起，您暂时不能留言！"}))

    if not username:
        return make_response(jsonify({"code" : 1, "message" : "请填写用户名称！"}))

    if not email:
        return make_response(jsonify({"code": 1, "message": "请填写您的邮件地址！"}))

    if not content:
        return make_response(jsonify({"code": 1, "message": "请填写您的留言内容！"}))

    if not cparent:
        cparent = 0

    article = db.session.query(Article).filter(Article.article_title==comment_article_title).first()
    if not article:
        return make_response(jsonify({"code": 1, "messge": "[err02] - 对不起，您暂时不能留言！"}))
    try:
        comment = Comment(
            comment_type = comment_type,
            comment_article_title =comment_article_title,
            comment_parent = cparent,
            comment_username = username,
            comment_email = email,
            comment_url = url,
            comment_content = content,
            comment_ip = "{}".format( request.remote_addr )
        )

        db.session.add(comment)
        db.session.commit()
        return make_response(jsonify({"code" : 0, "message" : "提交成功，您的评论将在审核通过后显示！"}))
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()
        return make_response(jsonify({"code": 1, "message": "提交失败，请稍后再试！"}))



