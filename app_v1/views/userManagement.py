# -*- coding: utf-8 -*-
"""
Create Time: 2021/3/3 14:19
Author: langkai
File: userManagement
"""
import uuid
from flask import Blueprint, session
from flask import request
from flask.json import jsonify
from .. import db
from .. import models

api = Blueprint('User', __name__)


def get_file_name():
    return str(uuid.uuid4())


@api.route("getList", methods=['POST'])
def userManagement_getList():
    """
        swagger_from_file: ./swagger_apis/User/User_getList.yml
        :return:
    """

    # if session.get('role'):
    res = dict()
    res['code'] = 200
    res['data'] = []
    res['msg'] = "success"
    print(request.json)
    pageNo = request.json.get("pageNo")
    pageSize = request.json.get("pageSize")
    name = request.json.get("name")
    value = request.json.get("value")
    table = getattr(models, api.name)
    res_list = db.session.query(table)
    if name:
        try:
            columns_type = getattr(table, name).property.columns[0].type.python_type
            obj = dict()
            obj[name] = columns_type(value)
            res_list = res_list.filter_by(**obj)
        except AttributeError as e:
            res['code'] = 500
            res['msg'] = e
            return jsonify(res)
        except TypeError as e:
            res['code'] = 500
            res['msg'] = e
            return jsonify(res)
    res_list = res_list.paginate()
    res = dict()
    res['code'] = 200
    res['data'] = []
    for i in res_list.items:
        obj = i.to_json()

        obj['permissions'] = ["管理员"] if i.role == "管理员" else ["用户"]
        avatar = obj['avatar'] if obj['avatar'] else "default.gif"
        obj['avatar'] = "static/avatar/{}".format(avatar)
        if i.ststus:
            obj["ststus"] = "正常用户"
        else:
            obj["ststus"] = "禁用用户"
        res['data'].append(obj)
    res['msg'] = "success"
    res['totalCount'] = res_list.total
    return jsonify(res)

    # else:
    #     return jsonify({"code": 403, "msg": "无权限"})


@api.route("getList1", methods=['POST'])
def userManagement_getList1():
    """
        swagger_from_file: ./swagger_apis/YingManagement_getOperations.yml
        :return:
    """
    # if session.get('role'):
    res = dict()
    res['code'] = 200
    res['data'] = []
    res['msg'] = "success"
    print(request.json)
    pageNo = request.json.get("pageNo")
    pageSize = request.json.get("pageSize")
    name = request.json.get("name")
    value = request.json.get("value")
    table = getattr(models, "Theme")
    res_list = db.session.query(table)
    if name:
        try:
            columns_type = getattr(table, name).property.columns[0].type.python_type
            obj = dict()
            obj[name] = columns_type(value)
            print(**obj)
            res_list = res_list.filter_by(**obj)
        except AttributeError as e:
            res['code'] = 500
            res['msg'] = e
            return jsonify(res)
        except TypeError as e:
            res['code'] = 500
            res['msg'] = e
            return jsonify(res)
    res_list = res_list.paginate(pageNo, per_page=pageSize)
    res = dict()
    res['code'] = 200
    res['data'] = []
    for i in res_list.items:
        obj = i.to_json()
        obj['user'] = i.publish_user.username
        res['data'].append(obj)
    res['msg'] = "success"
    res['totalCount'] = res_list.total
    return jsonify(res)

    # else:
    #     return jsonify({"code": 403, "msg": "无权限"})


@api.route("doEdit", methods=['POST'])
def userManagement_doEdit():
    """
        swagger_from_file: ./swagger_apis/YingManagement_getOperations.yml
        :return:
    """
    # if session.get('role'):
    id = request.json.get("id")
    password = request.json.get("password")
    username = request.json.get("username")
    if request.json.get("ststus") in ['正常用户', '禁止用户']:
        ststus = True if request.json.get("ststus") == "正常用户" else False
    else:
        return jsonify({"code": 503, "msg": "参数错误"})
    if request.json.get("permissions")[0] in ['用户','管理员']:
        role = "用户" if request.json.get("permissions")[0] == "用户" else "管理员"
    else:
        return jsonify({"code": 503, "msg": "参数错误"})
    print(request.json)
    user_editor = db.session.query(models.User).filter_by(id=id).first()
    if user_editor:
        if password:
            user_editor.password = password
        user_editor.username = username
        user_editor.ststus = ststus
        user_editor.role = role
        db.session.commit()
        return jsonify({"code": 200, "msg": "修改成功"})
    else:
        return jsonify({"code": 404, "msg": "未找到用户"})
    # else:
    #     return jsonify({"code": 403, "msg": "无权限"})


@api.route("doDelete", methods=['POST'])
def userManagement_doDelete():
    """
        swagger_from_file: ./swagger_apis/YingManagement_getOperations.yml
        :return:
    """
    if session.get('role') == "管理员":
        id = request.json.get("ids")
        if isinstance(id, int):
            obj = db.session.query(models.User).filter_by(id=id).first()
            db.session.delete(obj)
        elif isinstance(id, str):
            ids = id.split(",")
            for i in ids:
                obj = db.session.query(models.User).filter_by(id=int(i)).first()
                db.session.delete(obj)
            db.session.commit()
            return jsonify({"code": 200, "msg": "success"})
        else:
            return jsonify({"code": 200, "msg": "error"})
    else:
        return jsonify({"code": 403, "msg": "无权限"})
