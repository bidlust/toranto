#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>


from flask import make_response, render_template, jsonify, request, flash, session
from . import navigate
from app import db
from app.models import Navigate
from sqlalchemy.sql import func
from app.funlib import *

@navigate.route('/lists/', methods=['POST', 'GET'])
@auth_required
def navigate_lists():

    if request.method == 'POST':
        try:
            pageSize    =    int( request.form.get('pageSize') )
            pageNumber  =    int( request.form.get('pageNumber') )
        except Exception:
            pageSize =  app.config.get('PAGE_SIZE')
            pageNumber = 1
        params = []
        params.append(Navigate.deleted_at==None)
        if session.get('username') != 'root':
            params.append(Navigate.navigate_creator == session.get('username'))

        pagination = db.session.query(
            Navigate.id,
            Navigate.navigate_name,
            Navigate.navigate_url,
            Navigate.navigate_tag,
            Navigate.navigate_icon,
            Navigate.sq,
            Navigate.valid,
            func.date_format(Navigate.created_at, "%Y-%m-%d %H:%m:%S")
        ).filter(*params) \
            .order_by(Navigate.created_at.desc()) \
            .paginate(pageNumber, per_page=pageSize, error_out=True)

        total = pagination.total
        items = pagination.items
        title = ['id','navigate_name', 'navigate_url', 'navigate_tag', 'navigate_icon','sq','valid', 'created_at']
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_SUCCESS_CODE'),
            "message" : app.config.get('RESPONSE_SUCCESS_MESSAGE'),
            "rows": zip_dict(title, list(items)),
            "total": total
        }))
    return render_template('navigate.html')


@navigate.route('/add/', methods=['POST'])
def navigate_add():

    navigate_name = request.form.get('navigate_name')
    navigate_icon = request.form.get('navigate_icon')
    navigate_url = request.form.get('navigate_url')
    navigate_tag = request.form.get('navigate_tag')
    sq = request.form.get('sq') or 1
    valid = request.form.get('valid') or '0'

    if not navigate_name:
        return make_response(jsonify({"code" : 1, "message" : "导航名称为空！"}))
    if not navigate_icon:
        return make_response(jsonify({"code" : 1, "message" : "icon为空！"}))
    if not navigate_url:
        return make_response(jsonify({"code" : 1, "message" : "URL为空！"}))
    if not navigate_tag:
        return make_response(jsonify({"code" : 1, "message" : "Tag为空！"}))

    try:
        navigate = Navigate(
            navigate_name=navigate_name,
            navigate_icon=navigate_icon,
            navigate_url=navigate_url,
            navigate_tag=navigate_tag,
            navigate_creator = session.get('username'),
            sq=sq,
            valid=valid
        )
        db.session.add(navigate)
        db.session.commit()
        db.session.close()
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_SUCCESS_CODE'),
            "message": app.config.get('RESPONSE_SUCCESS_MESSAGE')
        }))
    except Exception as e:
        db.session.rollback()
        app.logger.exception(e)
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_ERROR_CODE'),
            "message": app.config.get('RESPONSE_ERROR_MESSAGE')
        }))
    finally:
        pass


@navigate.route('/delete/', methods=['GET'])
def navigate_delete():

    id = request.args.get('id')
    if not id:
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_PARAM_ERROR_CODE'),
            "message": app.config.get('RESPONSE_PARAM_ERROR_MESSAGE')
        }))
    try:
        db.session.query(Navigate).filter(Navigate.id==id).update({'deleted_at': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        db.session.commit()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_SUCCESS_CODE'), "message": app.config.get('RESPONSE_SUCCESS_MESSAGE')}))
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_ERROR_CODE'), "message": app.config.get('RESPONSE_ERROR_MESSAGE')}))
    finally:
        db.session.close()


@navigate.route('/invalid/', methods=['GET'])
def navigate_invalid():

    id = request.args.get('id')
    if not id:
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_PARAM_ERROR_CODE'),
            "message": app.config.get('RESPONSE_PARAM_ERROR_MESSAGE')
        }))
    try:
        db.session.query(Navigate).filter(Navigate.id==id).update({"valid" : "0"})
        db.session.commit()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_SUCCESS_CODE'), "message": app.config.get('RESPONSE_SUCCESS_MESSAGE')}))
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_ERROR_CODE'), "message": app.config.get('RESPONSE_ERROR_MESSAGE')}))


@navigate.route('/valid/', methods=['GET'])
def navigate_valid():

    id = request.args.get('id')
    if not id:
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_PARAM_ERROR_CODE'),
            "message": app.config.get('RESPONSE_PARAM_ERROR_MESSAGE')
        }))
    try:
        db.session.query(Navigate).filter(Navigate.id==id).update({"valid" : "1"})
        db.session.commit()
        return make_response(jsonify(
            {"code": app.config.get('RESPONSE_SUCCESS_CODE'), "message": app.config.get('RESPONSE_SUCCESS_MESSAGE')}))
    except Exception as e:
        app.logger.exception(e)
        db.session.rollback()
        return make_response(jsonify({"code": app.config.get('RESPONSE_ERROR_CODE'), "message": app.config.get('RESPONSE_ERROR_MESSAGE')}))
    finally:
        db.session.close()
