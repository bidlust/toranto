#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>


from flask import Blueprint, session, request, make_response, jsonify, abort
from app import db
from app.models import TorantoSetting
web = Blueprint('web', __name__, template_folder='pages')

@web.before_request
def web_before_request():

    skin = session.get('skin')
    if not skin:
        # get blog skin
        setting_skin = db.session.query(TorantoSetting.value).filter(TorantoSetting.valid == '1', TorantoSetting.key == 'site_skin').first()
        if setting_skin:
            session['skin'] = setting_skin[0]
        else:
            session['skin'] = 'default'

    # settings
    if not session.get('setting'):
        site_setting = db.session.query(TorantoSetting.key, TorantoSetting.value).filter(TorantoSetting.valid == '1').all()
        session['setting'] = {k: v for (k, v) in site_setting}


from . import index
from . import article