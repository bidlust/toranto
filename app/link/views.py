#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>


from flask import make_response, render_template, jsonify, request, flash, session
from . import link
from app import db
from app.models import Link
from sqlalchemy.sql import func
from app.funlib import *

@link.route('/lists/', methods=['POST', 'GET'])
@auth_required
def link_lists():

    if request.method == 'POST':
        try:
            pageSize    =    int( request.form.get('pageSize') )
            pageNumber  =    int( request.form.get('pageNumber') )
        except Exception:
            pageSize =  app.config.get('PAGE_SIZE')
            pageNumber = 1
        params = []
        params.append(Link.deleted_at==None)
        pagination = db.session.query(
            Link.id,
            Link.link_name,
            Link.link_href,
            Link.link_desc,
            Link.link_creator,
            Link.link_field,
            Link.valid,
            func.date_format(Link.created_at, "%Y-%m-%d %H:%m:%S")
        ).filter(*params) \
            .order_by(Link.created_at.desc()) \
            .paginate(pageNumber, per_page=pageSize, error_out=True)

        total = pagination.total
        items = pagination.items
        title = ['id','link_name', 'link_href', 'link_desc', 'link_creator','link_field','valid', 'created_at']
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_SUCCESS_CODE'),
            "message" : app.config.get('RESPONSE_SUCCESS_MESSAGE'),
            "rows": zip_dict(title, list(items)),
            "total": total
        }))
    return render_template('link.html')

@link.route('/delete/', methods=['GET'])
def link_delete():

    id = request.args.get('id')
    if not id:
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_PARAM_ERROR_CODE'),
            "message": app.config.get('RESPONSE_PARAM_ERROR_MESSAGE')
        }))
    try:
        db.session.query(Link).filter(Link.id==id).update({'deleted_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        db.session.commit()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_SUCCESS_CODE'), "message": app.config.get('RESPONSE_SUCCESS_MESSAGE')}))
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_ERROR_CODE'), "message": app.config.get('RESPONSE_ERROR_MESSAGE')}))



@link.route('/invalid/', methods=['GET'])
def link_invalid():

    id = request.args.get('id')
    if not id:
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_PARAM_ERROR_CODE'),
            "message": app.config.get('RESPONSE_PARAM_ERROR_MESSAGE')
        }))
    try:
        db.session.query(Link).filter(Link.id==id).update({"valid" : "0"})
        db.session.commit()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_SUCCESS_CODE'), "message": app.config.get('RESPONSE_SUCCESS_MESSAGE')}))
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_ERROR_CODE'), "message": app.config.get('RESPONSE_ERROR_MESSAGE')}))


@link.route('/valid/', methods=['GET'])
def link_valid():

    id = request.args.get('id')
    if not id:
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_PARAM_ERROR_CODE'),
            "message": app.config.get('RESPONSE_PARAM_ERROR_MESSAGE')
        }))
    try:
        db.session.query(Link).filter(Link.id==id).update({"valid" : "1"})
        db.session.commit()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_SUCCESS_CODE'), "message": app.config.get('RESPONSE_SUCCESS_MESSAGE')}))
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_ERROR_CODE'), "message": app.config.get('RESPONSE_ERROR_MESSAGE')}))
