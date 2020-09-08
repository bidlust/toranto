#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>


from flask import make_response, render_template, jsonify, request, session
from werkzeug.security import generate_password_hash
from . import article
from app import db
from app.models import Article, Category, Pwdmap
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
            Article.id,
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
        title = ['id','title', 'created', 'author', 'click', 'top', 'iscomment', 'ispublish', 'isvisible', 'ispassword']
        return make_response(jsonify({"code" : 0, "rows": zip_dict(title, list( items ) ) , "total":total}))

    return render_template('article.html')


@article.route('/create/', methods=['POST', 'GET'])
def article_create():
    if request.method == 'POST':
        ispublish = request.form.get('action') or app.config.get('ARTICLE_IS_PUBLISH')
        isvisible = request.form.get('isvisible') or app.config.get('ARTICLE_IS_VISIBLE')
        category = request.form.get('article_category') or app.config.get('ARTICLE_CATEGORY')
        title = request.form.get('article_title') or app.config.get('ARTICLE_TITLE')
        seo = request.form.get('article_seo') or app.config.get('ARTICLE_SEO')
        author = request.form.get('article_author') or app.config.get('ARTICLE_AUTHOR')
        date_expire = request.form.get('date_expire') or app.config.get('ARTICLE_EXPIRE_DATE')
        picture = request.form.get('article_picture') or app.config.get('ARTICLE_PICTURE')
        desc = request.form.get('article_desc') or app.config.get('ARTICLE_DESC')
        content = request.form.get('article_content') or app.config.get('ARTICLE_CONTENT')
        tags = request.form.get('article_tag') or app.config.get('ARTICLE_TAG')
        click = request.form.get('article_click') or app.config.get('ARTICLE_CLICK')
        sq = request.form.get('article_sq') or app.config.get('ARTICLE_SQ')
        top = request.form.get('top') or app.config.get('ARTICLE_IS_TOP')
        iscomment = request.form.get('iscomment') or app.config.get('ARTICLE_IS_COMMENT')
        istoolbar = request.form.get('istoolbar') or app.config.get('ARTICLE_IS_TOOLBAR')
        password = request.form.get('article_password') or app.config.get('ARTICLE_PASSWORD')
        price = request.form.get('article_price') or app.config.get('ARTICLE_PRICE')
        praise = request.form.get('article_praise') or app.config.get('ARTICLE_PRAISE')
        step = request.form.get('article_step') or app.config.get('ARTICLE_STEP')

        if not title:
            return make_response(jsonify({
                "code": 1,
                "message": "请输入文章标题！"
            }))
        if not content:
            return make_response(jsonify({
                "code": 1,
                "message": "请输入文章内容！"
            }))
        if not author:
            return make_response(jsonify({
                "code": 1,
                "message": "请输入文章作者！"
            }))

        article = Article(
            article_category    =category,
            article_title       =title,
            article_author      =author,
            article_desc        =desc,
            article_content     =content,
            article_tag         =tags,
            article_click       =click,
            article_praise      =praise,
            article_step        =step,
            article_seo         =seo,
            article_picture     =picture,
            article_password    = generate_password_hash( password ),
            article_price       =price,
            sq                  =sq,
            top                 =top,
            iscomment           =iscomment,
            ispublish           =ispublish,
            isvisible           =isvisible,
            istoolbar           =istoolbar,
            date_expire         =date_expire
        )
        article_mp = None
        if password:
            article_mp = Pwdmap(title=title, pwd=password)

        try:
            db.session.add(article)
            if article_mp:
                db.session.add(article_mp)
            db.session.commit()
            return make_response(jsonify({
                "code": app.config.get('ARTICLE_ADD_SUCCESS_CODE'),
                "message": app.config.get('ARTICLE_ADD_SUCCESS_MESSAGE')
            }))

        except Exception as e:
            app.logger.exception(e)
            db.session.rollback()
            return make_response(jsonify({
                "code": app.config.get('ARTICLE_ADD_ERROR_CODE'),
                "message": app.config.get('ARTICLE_ADD_ERROR_MESSAGE')
            }))

        finally:
            pass


    # article category
    category = Category.query.with_entities(Category.category_name).filter(Category.deleted_at == None, Category.valid == '1').all()

    #编辑；
    aid = request.args.get('aid')
    article_obj = None
    if aid:
        article_obj = db.session.query(
            Article.id,
            Article.article_title,
            Article.article_category,
            Article.article_seo,
            Article.article_author,
            Article.date_expire,
            Article.article_picture,
            Article.article_desc,
            Article.article_content,
            Article.article_tag,
            Article.article_click,
            Article.sq,
            Pwdmap.pwd,
            Article.article_price,
            Article.article_praise,
            Article.article_step,
            Article.top,
            Article.iscomment,
            Article.isvisible,
            Article.istoolbar
        ).outerjoin(
            Pwdmap,
            Pwdmap.title==Article.article_title
        ).filter(Article.id==aid).first()
        db.session.commit()
    return render_template('article_create.html', category=category, article_obj=article_obj)



@article.route('/getUeditorConfig/', methods=['GET'])
def article_getUeditorConfig():

    return make_response(jsonify({
            "imageUrl": '',
            "imagePath": "",
            "imageFieldName": "upfile",
            "imageMaxSize": 2048,
            "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],
    }))
