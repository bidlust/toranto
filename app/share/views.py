#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>


from flask import make_response, render_template, jsonify, request, flash, session
from . import share
from app import db
from app.models import Share
from sqlalchemy.sql import func
from app.funlib import *

@share.route('/lists/', methods=['POST', 'GET'])
@auth_required
def share_lists():

    if request.method == 'POST':
        try:
            pageSize    =    int( request.form.get('pageSize') )
            pageNumber  =    int( request.form.get('pageNumber') )
        except Exception:
            pageSize =  app.config.get('PAGE_SIZE')
            pageNumber = 1
        params = []
        params.append(Share.deleted_at==None)
        pagination = db.session.query(
            Share.id,
            Share.share_name,
            Share.share_click,
            Share.share_download,
            Share.share_creator,
            Share.share_link,
            Share.share_location,
            Share.share_password,
            Share.share_price,
            Share.share_type,
            Share.valid,
            func.date_format(Share.created_at, "%Y-%m-%d %H:%m:%S")
        ).filter(*params) \
            .order_by(Share.share_click.desc(), Share.share_download.desc()) \
            .paginate(pageNumber, per_page=pageSize, error_out=True)

        total = pagination.total
        items = pagination.items
        title = ['id','share_name', 'share_click', 'share_download', 'share_creator','share_link','share_location', 'share_password', 'share_price', 'share_type', 'valid', 'created_at']
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_SUCCESS_CODE'),
            "message" : app.config.get('RESPONSE_SUCCESS_MESSAGE'),
            "rows": zip_dict(title, list(items)),
            "total": total
        }))
    get_page_name()
    return render_template('share.html')

@share.route('/delete/', methods=['GET'])
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



@share.route('/invalid/', methods=['GET'])
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


@share.route('/valid/', methods=['GET'])
def share_valid():

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
