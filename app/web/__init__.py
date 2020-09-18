#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>


from flask import Blueprint, session, request, make_response, jsonify, abort

web = Blueprint('web', __name__, template_folder='pages', url_prefix='/index')


from . import index
