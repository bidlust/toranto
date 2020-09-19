#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import make_response, render_template, jsonify, request, flash, session

from . import sitesetting
from app.models import TorantoSetting
from app import db, app

@sitesetting.route('/baseinfo/', methods=['POST', 'GET'])
def sitesetting_baseinfo():

    if request.method == 'POST':
        site_name = request.form.get('site_name') or ''
        site_active = request.form.get('site_active') or ''
        site_comment = request.form.get('site_comment') or ''
        site_title = request.form.get('site_title') or ''
        site_logo = request.form.get('site_logo') or ''
        site_keywords = request.form.get('site_keywords') or ''
        site_description = request.form.get('site_description') or ''
        site_foot = request.form.get('site_foot') or ''
        site_domain = request.form.get('site_domain') or ''
        site_icon = request.form.get('site_icon') or ''

        if not site_name:
            flash('请填写站点名称！', category='error')
        if not site_active:
            flash('请选择站点运行状态！', category='error')
        if not site_title:
            flash('请输入站点标题！', category='error')
        if not site_keywords:
            flash('请输入站点关键字！', category='error')
        if not site_description:
            flash('请输入站点描述！', category='error')

        if site_name and site_active and site_title and site_keywords and site_description:
            for k, v in request.form.to_dict().items():
                if 'site' in k:
                    sql = '''
                        insert into
                            toranto_setting
                        (
                            `key`,
                            `value`
                        )
                        values
                        (
                            '{}',
                            '{}'
                        )
                        on duplicate key update
                            `value`=values(`value`)
                    '''.format(
                        k,
                        v
                    )
                    db.session.execute(sql)
                    db.session.commit()
            flash('设置成功！', category='success')
    #site setting;
    settings = db.session.query(TorantoSetting.key, TorantoSetting.value).filter(TorantoSetting.valid=='1').all()
    setting_dict = { k:v for (k,v) in settings }

    #skin;
    skins = app.config.get('SKINS')

    return render_template('setting.html', settings=setting_dict, skins=skins)


