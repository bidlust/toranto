#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import make_response, render_template, jsonify, request, flash, session
from . import category
from app.models import TorantoSetting
from app import db
from app.models import Category
from flask import current_app as app
import datetime
from app.funlib import *
from sqlalchemy.sql import func


@category.route('/lists/', methods=['POST', 'GET'])
def category_lists():
    if request.method == 'POST':
        try:
            pageSize    =    int( request.form.get('pageSize') )
            pageNumber  =    int( request.form.get('pageNumber') )
        except Exception:
            pageSize =  app.config.get('PAGE_SIZE')
            pageNumber = 1
        params = []
        if not 'root' in session.get('role'):
            params.append(Category.category_creator==session.get('username'))

        pagination = db.session.query(
            Category.id,
            Category.category_name,
            Category.category_desc,
            Category.valid,
            func.date_format(Category.created_at, "%Y-%m-%d %H:%m:%S"),
        ).filter(*params) \
            .order_by(Category.created_at.desc()) \
            .paginate(pageNumber, per_page=pageSize, error_out=True)

        total = pagination.total
        items = pagination.items
        title = ['id','category_name', 'category_desc', 'valid', 'created_at']
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_SUCCESS_CODE'),
            "message" : app.config.get('RESPONSE_SUCCESS_MESSAGE'),
            "rows": zip_dict(title, list(items)),
            "total": total
        }))
    return render_template('category.html')


@category.route('/add/', methods=['POST'])
def category_add():
    category_name = request.form.get('category_name')
    category_desc = request.form.get('category_desc')
    isvalid = request.form.get('isvalid') or '1'

    if not category_name:
        return make_response(jsonify({"code" : 1, "message" : "请填写分类名称！"}))

    try:
        category = Category(
            category_name=category_name,
            category_desc=category_desc,
            category_creator=session.get('username'),
            valid=isvalid
        )
        db.session.add(category)
        db.session.commit()
        return make_response(jsonify({"code": app.config.get('RESPONSE_SUCCESS_CODE'), "message": app.config.get('RESPONSE_SUCCESS_MESSAGE')}))
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()
        return make_response(jsonify({"code": app.config.get('RESPONSE_ERROR_CODE'), "message": app.config.get('RESPONSE_ERROR_MESSAGE')}))

@category.route('/delete/', methods=['GET'])
def category_delete():

    id = request.args.get('id')
    if not id:
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_PARAM_ERROR_CODE'),
            "message": app.config.get('RESPONSE_PARAM_ERROR_MESSAGE')
        }))
    try:
        db.session.query(Category).filter(Category.id==id).delete()
        db.session.commit()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_SUCCESS_CODE'), "message": app.config.get('RESPONSE_SUCCESS_MESSAGE')}))
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_ERROR_CODE'), "message": app.config.get('RESPONSE_ERROR_MESSAGE')}))



@category.route('/invalid/', methods=['GET'])
def category_invalid():

    id = request.args.get('id')
    if not id:
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_PARAM_ERROR_CODE'),
            "message": app.config.get('RESPONSE_PARAM_ERROR_MESSAGE')
        }))
    try:
        db.session.query(Category).filter(Category.id==id, Category.category_creator==session.get('username')).update({"valid" : "0"})
        db.session.commit()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_SUCCESS_CODE'), "message": app.config.get('RESPONSE_SUCCESS_MESSAGE')}))
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_ERROR_CODE'), "message": app.config.get('RESPONSE_ERROR_MESSAGE')}))


@category.route('/valid/', methods=['GET'])
def category_valid():

    id = request.args.get('id')
    if not id:
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_PARAM_ERROR_CODE'),
            "message": app.config.get('RESPONSE_PARAM_ERROR_MESSAGE')
        }))
    try:
        db.session.query(Category).filter(Category.id==id, Category.category_creator==session.get('username')).update({"valid" : "1"})
        db.session.commit()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_SUCCESS_CODE'), "message": app.config.get('RESPONSE_SUCCESS_MESSAGE')}))
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_ERROR_CODE'), "message": app.config.get('RESPONSE_ERROR_MESSAGE')}))
