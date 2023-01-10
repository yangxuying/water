# -*- coding: utf-8 -*-
# @Time : 2019/10/28 15:49
# @Author : LangKai
# @Site : 
# @File : models.py
# @Software: PyCharm
import base64
import os
import uuid

from flask import Blueprint, session
from flask import request
from flask.json import jsonify
import json
from .. import db
from .. import models
from .. import redis_client
import cv2

user = Blueprint('user', __name__)


def get_file_name():
    return str(uuid.uuid4())


@user.route('/login', methods=['POST'])
def login():
    """
        swagger_from_file: ./swagger_apis/User/User_login.yml
        :return:
    """
    if request.method == "POST":
        username = request.json.get("username")
        user = db.session.query(models.User).filter_by(username=username).first()
        if not user:
            return jsonify({"code": 404, "msg": "This user does not exist", "redirect": "/404"})
        password = request.json.get("password")
        if not user.check_password_hash(password):
            return jsonify({"code": 404, "msg": "Password error", "redirect": "/404"})
        if not user.ststus or not user.role:
            return jsonify({"code": 401, "msg": "User disabled, please contact the administrator", "redirect": "/401"})
        session['role'] = user.role
        session['name'] = user.username
        session['login'] = 'yes'
        session['id'] = user.id

        session['avatar'] = user.avatar

        return jsonify({"code": 200, "msg": "success", "data": {"accessToken": user.id}})


@user.route("/userInfo", methods=['POST'])
def userInfo():
    """
        swagger_from_file: ./swagger_apis/User/User_info.yml
        :return:
    """
    # user_id = request.json.get("accessToken")
    # if session.get("name"):
    ret = dict()
    ret['code'] = 200
    ret['msg'] = 'success'
    name = session.get("name")
    permissions = session.get("role")
    avatar = session['avatar'] if session.get('avatar') is not None else "default.gif"
    print(avatar)
    ret['data'] = {
        "permissions": [permissions],
        "username": name,
        "avatar": "static/avatar/{}".format(avatar)}
    # else:
    #     ret = dict()
    #     ret['code'] = 200
    #     ret['msg'] = '无用户信息'
    return jsonify(ret)


@user.route("/userinfo_", methods=['POST'])
def userinfo_():

    id = session.get("id")
    user = db.session.query(models.User).filter_by(id=id).first()
    form = user.to_json()
    # avatar = session['avatar'] if session['avatar'] else "default.gif"
    avatar = session['avatar'] if session.get('avatar') is not None else "default.gif"
    form['avatar'] = "static/avatar/{}".format(avatar)
    ret = {'code': 200, 'form': form, 'iconList': [], 'filesum': []}
    return jsonify(ret)


@user.route("/islogin", methods=['GET'])
def islogin():
    """
        swagger_from_file: ./swagger_apis/User/User_islogin.yml
        :return:
    """
    is_login = session.get("login")
    if is_login == 'yes':
        ret = {'code': 200, 'is_login': True, 'msg': 'success'}
    else:
        ret = {'code': 200, 'is_login': False, 'msg': 'success'}
    return jsonify(ret)


@user.route("/logout", methods=['POST'])
def login_out():
    """
        swagger_from_file: ./swagger_apis/User/User_logout.yml
        :return:
    """
    if request.method == 'POST':
        session.clear()

        return jsonify({'code': 200, 'data': [], 'msg': "退出成功"})
    else:
        return jsonify({'code': -1})


@user.route("/register", methods=['POST'])
def register():
    """
        swagger_from_file: ./swagger_apis/User/User_register.yml
        :return:
    """
    if request.method == "POST":
        r = request.json
        print(request.json)
        username = r.get("username")
        password = r.get("password")
        if username == "匿名用户":
            return jsonify({"code": -1, "msg": "用户名禁止注册"})
        user = db.session.query(models.User).filter_by(username=username).first()
        if user:
            return jsonify({"code": -1, "msg": "用户名已存在"})

        new_user = models.User()
        new_user.username = username
        new_user.password = password
        new_user.role = "管理员"
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"code": 200, 'data': [], "msg": "注册成功", })


@user.route("/changePassword", methods=['POST'])
def changePassword():
    """
        swagger_from_file: ./swagger_apis/User/User_changePassword.yml
        :return:
    """
    if request.method == "POST":
        r = request.json
        phone = r.get("phone")
        username = r.get("username")
        password = r.get("password")
        code = r.get("code")
        user = db.session.query(models.User).filter_by(username=username, phone=phone, code=code).first()
        if user:
            user.password = password
            db.session.commit()
            return jsonify({"code": 200, 'date': [], "msg": "Password modified successfully"})
        else:
            return jsonify({"code": -1, 'date': [], "msg": "User information error"})


@user.route("/editAvatar", methods=['POST'])
def editAvatar():
    """
        swagger_from_file: ./swagger_apis/User/User_editAvatar.yml
        :return:
    """
    r = request.json
    img_data = base64.b64decode(r.get("img").split('data:image/png;base64,')[-1])
    pic_name = get_file_name()
    ur = "static/avatar/{}.png".format(pic_name)
    with open(ur, 'wb') as f:
        f.write(img_data)
    upload = '{}.png'.format(pic_name)
    user = db.session.query(models.User).filter_by(id=session.get("id")).first()
    user.avatar = upload
    session['avatar'] = upload
    db.session.commit()
    return jsonify(
        {"code": 200, "msg": "Modified successfully", 'url': "static/avatar/{}".format(upload)})


@user.route("/upload_pic", methods=['POST'])
def upload_pic():
    """
        swagger_from_file: ./swagger_apis/User/User_uploadPic.yml
        :return:
    """
    file = request.files.get("file")
    if file.filename.split(".")[-1] in ['jpg', 'png', 'JPG', 'PNG']:
        new_file_name = "{}.{}".format(get_file_name(), file.filename.split(".")[-1])
        file.save(os.path.join("static/upload", new_file_name))
    else:
        return jsonify({"code": 503, "msg": "图片类型错误"})
    return jsonify({"code": 200, "msg": "上传成功", "url": "static/upload/{}".format(new_file_name)})


def get_video_duration(filename):
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        rate = cap.get(5)
        frame_num = cap.get(7)
        duration = frame_num / rate
        return duration
    return -1


@user.route("/upload_video", methods=['POST'])
def upload_video():
    """
        swagger_from_file: ./swagger_apis/User/User_uploadVideo.yml
        :return:
    """
    file = request.files.get("file")
    if file.filename.split(".")[-1] in ['mp4', 'MP4']:
        new_file_name = "{}.{}".format(get_file_name(), file.filename.split(".")[-1])
        file.save(os.path.join("static/upload", new_file_name))
        dur = get_video_duration(os.path.join("static/upload", new_file_name))
        if dur != -1:
            m, s = divmod(int(dur), 60)
            h, m = divmod(m, 60)
            tm = "{0}:{1:02d}:{2:02d}".format(h, m, s)
        else:
            return jsonify({"code": 503, "msg": "视频错误"})
    else:
        return jsonify({"code": 503, "msg": "视频类型错误"})
    return jsonify({"code": 200, "msg": "上传成功", "url": "static/upload/{}".format(new_file_name), "tm": tm})
