#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>


from flask import Blueprint, session, request, make_response, jsonify, abort

navigate = Blueprint('navigate', __name__, template_folder='pages', url_prefix='/navigate')


@navigate.before_request
def article_before_request():
    if not session.get('auth'):
        if request.is_xhr:
            return make_response(jsonify({"code": 1, "message": "Unauthorized！"}))
        abort(401)


from . import views


