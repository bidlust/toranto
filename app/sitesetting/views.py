#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import make_response, render_template, jsonify, request, flash, session

from . import sitesetting
from app.models import TorantoSetting
from app import db

@sitesetting.route('/baseinfo/', methods=['POST', 'GET'])
def sitesetting_baseinfo():

    if request.method == 'POST':
        site_name = request.form.get('site_name')
        site_active = request.form.get('site_active')
        site_comment = request.form.get('site_comment')
        site_title = request.form.get('site_title')
        site_logo = request.form.get('site_logo')
        site_keywords = request.form.get('site_keywords')
        site_description = request.form.get('site_description')
        site_foot = request.form.get('site_foot')
        site_domain = request.form.get('site_domain')
        created_by = session.get('username')
        if not site_name:
            flash('请填写站点名称！', category='error')
        if site_name:
            sql = '''
                insert into
                    `toranto_setting`
                (
                    `site_name`,
                    `site_active`,
                    `site_comment`,
                    `site_title`,
                    `site_logo`,
                    `site_keywords`,
                    `site_description`,
                    `site_foot`,
                    `site_domain`,
                    `created_by`
                )
                values
                (
                    '{}',
                    {},
                    {},
                    {},
                    {},
                    {},
                    {},
                    {},
                    {},
                    '{}'
                )
                on duplicate key update
                    `site_name`     = values(`site_name`),
                    `site_active`   = values(`site_active`),
                    `site_comment`  = values(`site_comment`),
                    `site_title`    = values(`site_title`),
                    `site_logo`     = values(`site_logo`),
                    `site_keywords` = values(`site_keywords`),
                    `site_description`= values(`site_description`),
                    `site_foot`     = values(`site_foot`),
                    `site_domain`   = values(`site_domain`)
            '''.format(
                    site_name,
                    "'{}'".format( site_active ) if site_active else 'NULL',
                    "'{}'".format(site_comment) if site_comment else 'NULL',
                    "'{}'".format(site_title) if site_title else 'NULL',
                    "'{}'".format(site_logo) if site_logo else 'NULL',
                    "'{}'".format(site_keywords) if site_keywords else 'NULL',
                    "'{}'".format(site_description) if site_description else 'NULL',
                    "'{}'".format(site_foot) if site_foot else 'NULL',
                    "'{}'".format(site_domain) if site_domain else 'NULL',
                    created_by
            )
            db.session.execute( sql )
            db.session.commit()
            flash('设置成功！', category='success')

    settings = TorantoSetting.query.filter_by(created_by=session.get('username')).first()

    return render_template('setting.html', settings=settings)


