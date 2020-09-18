#!/usr/bin/env python3
# by dongchao <cookie@maxcale.cn>

from flask import request, make_response, jsonify, url_for
from flask import current_app as app
from . import action
import datetime
from app.funlib import *
import os
from app.models import Uploadfile, Attachment
from app import db, csrf


def get_upload_path():
    upload_path = os.path.join(
        app.config.get('UPLOAD_PATH'),
        datetime.datetime.now().strftime("%Y-%m-%d")
    )
    return upload_path


#批量上传图片；
@action.route('/upload_images/', methods=['POST'])
def action_upload_images():
    if request.method == 'POST':
        image_files = request.files.getlist('upload_images')
        if not image_files:
            return make_response(jsonify({
                "code" : app.config.get('RESPONSE_UPLOAD_ERROR_CODE'),
                "message" : app.config.get('RESPONSE_UPLOAD_ERROR_MESSAGE')
            }))
        images_list = []
        for image_file in image_files:
            image_name = image_file.filename
            file_type = os.path.splitext(image_name)[-1]
            if not file_type.lower() in app.config.get('IMAGE_ALLOWED'):
                return make_response(jsonify({
                    "code": app.config.get('RESPONSE_UPLOAD_NOT_ALLOW_CODE'),
                    "message": app.config.get('RESPONSE_UPLOAD_NOT_ALLOW_MESSAGE')
                }))
            upload_path = get_upload_path()
            if not os.path.exists(upload_path):
                os.makedirs(upload_path, 0o777)
            tmp_file_name = "{}{}".format(get_random(), file_type)
            image_file.save(os.path.join(upload_path, tmp_file_name))
            visit_path = os.path.join( datetime.datetime.now().strftime("%Y-%m-%d") , tmp_file_name)
            images_list.append(visit_path)
            upload = Uploadfile(
                upload_name     = '博客文章标题图片',
                upload_path     = upload_path,
                upload_type     = file_type,
                upload_size     = os.path.getsize( os.path.join(upload_path, tmp_file_name) ),
                upload_busi     = 'article_logo',
                upload_real     = image_name,
                upload_saved    = tmp_file_name,
                upload_creator  = session.get('username')
            )

            try:
                db.session.add(upload)
                db.session.commit()
            except Exception as e:
                app.logger.exception(e)
                return make_response(jsonify({
                    "code": app.config.get('RESPONSE_SAVE_ERROR_CODE'),
                    "message": app.config.get('RESPONSE_SAVE_ERROR_MESSAGE')
                }))
            finally:
                pass

        return make_response(jsonify({
            "code": app.config.get('RESPONSE_SAVE_SUCCESS'),
            "message": app.config.get('RESPONSE_SAVE_SUCCESS_MESSAGE'),
            "data" : images_list
        }))



#上传单张图片；
@action.route('/upload_image/', methods=['POST'])
def action_upload_image():
    if request.method == 'POST':
        image_file = request.files.get('upload_image')
        if not image_file:
            return make_response(jsonify({
                "code" : app.config.get('RESPONSE_UPLOAD_ERROR_CODE'),
                "message" : app.config.get('RESPONSE_UPLOAD_ERROR_MESSAGE')
            }))
        image_name = image_file.filename
        file_type = os.path.splitext(image_name)[-1]
        if not file_type.lower() in app.config.get('IMAGE_ALLOWED'):
            return make_response(jsonify({
                "code": app.config.get('RESPONSE_UPLOAD_NOT_ALLOW_CODE'),
                "message": app.config.get('RESPONSE_UPLOAD_NOT_ALLOW_MESSAGE')
            }))
        upload_path = get_upload_path()
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, 0o777)
        tmp_file_name = "{}{}".format(get_random(), file_type)
        image_file.save(os.path.join(upload_path, tmp_file_name))
        visit_path = os.path.join( "img", datetime.datetime.now().strftime("%Y-%m-%d") , tmp_file_name)
        image_size = os.path.getsize( os.path.join(upload_path, tmp_file_name) )
        upload = Uploadfile(
            upload_name     = '博客文章标题图片',
            upload_path     = upload_path,
            upload_type     = file_type,
            upload_size     = image_size,
            upload_busi     = 'article_logo',
            upload_real     = image_name,
            upload_saved    = tmp_file_name,
            upload_visit    = visit_path,
            upload_creator  = session.get('username')
        )

        try:
            db.session.add(upload)
            db.session.commit()
        except Exception as e:
            app.logger.exception(e)
            return make_response(jsonify({
                "code": app.config.get('RESPONSE_SAVE_ERROR_CODE'),
                "message": app.config.get('RESPONSE_SAVE_ERROR_MESSAGE')
            }))
        finally:
            pass

        return make_response(jsonify({
            "code": app.config.get('RESPONSE_SAVE_SUCCESS'),
            "message": app.config.get('RESPONSE_SAVE_SUCCESS_MESSAGE'),
            "url" : visit_path,
            "type" : file_type,
            "title" : image_name,
            "size" : image_size,
            "original" :  image_name,
            "state": "SUCCESS"
        }))





#上传单个文件；
@action.route('/upload_file/', methods=['POST'])
def action_upload_file():
    if request.method == 'POST':
        upload_file = request.files.get('upload_file')
        if not upload_file:
            return make_response(jsonify({
                "code" : app.config.get('RESPONSE_UPLOAD_ERROR_CODE'),
                "message" : app.config.get('RESPONSE_UPLOAD_ERROR_MESSAGE')
            }))
        file_name = upload_file.filename
        file_type = os.path.splitext(file_name)[-1]
        if not file_type.lower() in app.config.get('FILE_ALLOWED'):
            return make_response(jsonify({
                "code": app.config.get('RESPONSE_UPLOAD_NOT_ALLOW_CODE'),
                "message": app.config.get('RESPONSE_UPLOAD_NOT_ALLOW_MESSAGE')
            }))
        upload_path = get_upload_path()
        if not os.path.exists(upload_path):
            os.makedirs(upload_path, 0o777)
        tmp_file_name = "{}{}".format(get_random(), file_type)
        upload_file.save(os.path.join(upload_path, tmp_file_name))
        visit_path = os.path.join( "attach", datetime.datetime.now().strftime("%Y-%m-%d") , tmp_file_name)
        attach_size = os.path.getsize( os.path.join(upload_path, tmp_file_name) )
        upload = Uploadfile(
            upload_name     = '博客文章附件',
            upload_path     = upload_path,
            upload_type     = file_type,
            upload_size     = attach_size,
            upload_busi     = 'article_attachment',
            upload_real     = file_name,
            upload_saved    = tmp_file_name,
            upload_visit    = visit_path,
            upload_creator  = session.get('username')
        )

        try:
            db.session.add(upload)
            db.session.commit()
        except Exception as e:
            app.logger.exception(e)
            return make_response(jsonify({
                "code": app.config.get('RESPONSE_SAVE_ERROR_CODE'),
                "message": app.config.get('RESPONSE_SAVE_ERROR_MESSAGE')
            }))
        finally:
            pass

        attach = Attachment(

        )
        return make_response(jsonify({
            "code": app.config.get('RESPONSE_SAVE_SUCCESS'),
            "message": app.config.get('RESPONSE_SAVE_SUCCESS_MESSAGE'),
            "url" : visit_path,
            "type" : file_type,
            "title" : file_name,
            "size" : attach_size,
            "original" :  file_name,
            "state": "SUCCESS"
        }))




@csrf.exempt
@action.route('/ueditor/', methods=['GET', 'POST'])
def action_ueditor():
    action  = request.args.get('action')
    if not action:
        return  make_response(jsonify({
            "code" : "",
            "message" : ""
        }))
    if action == 'config':
        return make_response(jsonify({
            "imageUrl": url_for('action.action_upload_image'),
            "imagePath": get_upload_path(),
            "imageUrlPrefix" : app.config.get('SERVER_DOMAMIN'),
            "imageActionName" : "imageUpload",
            "imageFieldName": "upload_image",

            "imageMaxSize": 2048000,
            "videoMaxSize" : 2048000,
            "fileMaxSize": 20480000,
            "imageAllowFiles": app.config.get('IMAGE_ALLOWED'),

            "fileUrl" : url_for('action.action_upload_file'),
            "filePath": get_upload_path(),
            "fileUrlPrefix": app.config.get('SERVER_DOMAMIN'),
            "fileFieldName" : "upload_file",
            "fileActionName": "fileUpload",
            "fileAllowFiles": app.config.get('FILE_ALLOWED')


        }))
    elif action == 'imageUpload' :
        return action_upload_image()
    elif action == 'fileUpload':
        return action_upload_file()
    else:
        pass

