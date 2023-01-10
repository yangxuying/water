# -*- coding: utf-8 -*-
"""
Create Time: 2021/3/3 14:19
Author: langkai
File: userManagement
"""
import datetime
import uuid

import pandas as pd
from flask import Blueprint, session
from flask import request
from flask.json import jsonify

from utils.alo_one import data_clean, water_predict1, water_predict2
from .. import db
from .. import models

api = Blueprint('Data', __name__)


def get_file_name():
    return str(uuid.uuid4())


@api.route("getList", methods=['POST'])
def userManagement_getList():
    """
        swagger_from_file: ./swagger_apis/YingManagement_getOperations.yml
        :return:
    """
    # if session.get('role'):
    res = dict()

    pageNo = request.json.get("pageNo") or 1
    pageSize = request.json.get("pageSize") or 10
    name = request.json.get("name")
    value = request.json.get("value")
    table = getattr(models, api.name)
    res_list = db.session.query(table).order_by(table.测量时间.desc())

    try:
        if name:
            columns_type = getattr(table, name).property.columns[0].type.python_type
            if columns_type is float:
                p = db.session.execute('select * from data where trim({})={}'.format(name, value))
                res_list = p.fetchall()
                for i in res_list[(pageNo-1)*pageSize:(pageNo*pageSize)]:
                    obj = zip(['监测点', '测量时间', '水温', 'pH', '溶解氧', '电导率', '浊度', '高锰酸盐指数', '总磷', '总氮', '叶绿素', '蓝绿藻', '氨氮'],i)

                    res['data'].append(dict(obj))
                res['msg'] = "success"
                res['totalCount'] = len(res_list)
            elif columns_type is str:
                obj = dict()
                obj[name] = columns_type(value)
                res_list = res_list.filter_by(**obj)
                res_list = res_list.paginate(page=int(pageNo), per_page=int(pageSize))
                res['code'] = 200
                res['data'] = []
                for i in res_list.items:
                    obj = i.to_json()
                    res['data'].append(obj)
                res['msg'] = "success"
                res['totalCount'] = res_list.total
        else:
            res_list = res_list.paginate(page=int(pageNo), per_page=int(pageSize))
            res['code'] = 200
            res['data'] = []
            for i in res_list.items:
                obj = i.to_json()
                res['data'].append(obj)
            res['msg'] = "success"
            res['totalCount'] = res_list.total
    except AttributeError as e:
        res['code'] = 500
        res['msg'] = e
        return jsonify(res)
    except TypeError as e:
        res['code'] = 500
        res['msg'] = e
        return jsonify(res)

    return jsonify(res)

    # else:
    #     return jsonify({"code": 403, "msg": "无权限"})


chche = {}


@api.route("getList1", methods=['POST'])
def userManagement_getList1():
    """
        swagger_from_file: ./swagger_apis/YingManagement_getOperations.yml
        :return:
    """
    # if session.get('role'):
    r = request.json
    data = db.session.query(models.Data).order_by(models.Data.测量时间.desc()).all()
    riqi = data[0].测量时间
    riqi1 = riqi

    res = {}
    res['date'] = []
    for i in range(3):
        today = datetime.datetime.strptime(riqi, "%Y-%m-%d")
        next = today + datetime.timedelta(days=1)
        day = str(next.strftime("%Y-%m-%d"))
        res['date'].append(day)
        riqi = day

    data = data[::-1]
    data11 = [i.to_json() for i in data]

    data = pd.DataFrame(data11)
    data1 = data_clean(data, '溶解氧')
    if r.get("value") and r.get("value") in ['OnlineESN', 'MIC-OnlineESN']:
        predict_value11 = water_predict1(data1, '溶解氧')
    elif r.get("value") and r.get("value") in ['OfflineESN', 'MIC-OfflineESN']:
        predict_value11 = water_predict2(data1, '溶解氧')
    else:
        return jsonify({"code": 403, "msg": "无权限"})
    res['data1'] = {}
    res['data1']['yuce'] = [i[0] for i in predict_value11.tolist()]
    res['data1']['yuce_data'] = res['date']
    data1 = data_clean(data, '高锰酸盐指数')

    if r.get("value") and r.get("value") in ['OnlineESN', 'MIC-OnlineESN']:
        predict_value11 = water_predict1(data1, '高锰酸盐指数')
    elif r.get("value") and r.get("value") in ['OfflineESN', 'MIC-OfflineESN']:
        predict_value11 = water_predict2(data1, '高锰酸盐指数')
    else:
        return jsonify({"code": 403, "msg": "无权限"})
    res['data2'] = {}
    res['data2']['yuce'] = [i[0] for i in predict_value11.tolist()]
    res['data2']['yuce_data'] = res['date']
    data1 = data_clean(data, '总磷')
    if r.get("value") and r.get("value") in ['OnlineESN', 'MIC-OnlineESN']:
        predict_value11 = water_predict1(data1, '总磷')
    elif r.get("value") and r.get("value") in ['OfflineESN', 'MIC-OfflineESN']:
        predict_value11 = water_predict2(data1, '总磷')
    else:
        return jsonify({"code": 403, "msg": "无权限"})
    res['data3'] = {}
    res['data3']['yuce'] = [i[0] for i in predict_value11.tolist()]
    res['data3']['yuce_data'] = res['date']
    res['data1']['date'] = []
    res['data1']['date_data'] = []
    res['data2']['date'] = []
    res['data2']['date_data'] = []
    res['data3']['date'] = []
    res['data3']['date_data'] = []
    for i in range(7):
        res['data1']['date'].append(data11[::-1][i]['溶解氧'])
        res['data2']['date'].append(data11[::-1][i]['高锰酸盐指数'])
        res['data3']['date'].append(data11[::-1][i]['总磷'])
        res['data1']['date_data'].append(data11[::-1][i]['测量时间'])
        res['data2']['date_data'].append(data11[::-1][i]['测量时间'])
        res['data3']['date_data'].append(data11[::-1][i]['测量时间'])
    res['data1']['date'] = res['data1']['date'][::-1]
    res['data2']['date'] = res['data2']['date'][::-1]
    res['data3']['date'] = res['data3']['date'][::-1]

    res['data1']['date_data'] = res['data1']['date_data'][::-1]
    res['data2']['date_data'] = res['data2']['date_data'][::-1]
    res['data3']['date_data'] = res['data3']['date_data'][::-1]
    res["code"] = 200
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
    r = request.json
    if r.get("测量时间"):
        one = db.session.query(models.Data).filter_by(测量时间=r.get("测量时间")).first()
        one.add_to_json(r)
        db.session.commit()
        return jsonify({"code": 200, "msg": "修改成功"})
    else:
        res_list = db.session.query(models.Data).order_by(models.Data.测量时间.desc()).first()
        dat = res_list.测量时间
        today = datetime.datetime.strptime(dat, "%Y-%m-%d")
        next = today + datetime.timedelta(days=1)
        day = str(next.strftime("%Y-%m-%d"))
        r['测量时间'] = day
        new = models.Data()
        new.add_to_json(r)
        db.session.add(new)
        db.session.commit()
        return jsonify({"code": 200, "msg": "添加成功"})


@api.route("doDelete", methods=['POST'])
def userManagement_doDelete():
    """
        swagger_from_file: ./swagger_apis/YingManagement_getOperations.yml
        :return:
    """
    # if session.get('role') == "管理员":
    id = request.json.get("ids")
    if isinstance(id, int):
        obj = db.session.query(models.Data).filter_by(测量时间=id).first()
        db.session.delete(obj)
    elif isinstance(id, str):
        ids = id.split(",")
        for i in ids:
            obj = db.session.query(models.Data).filter_by(测量时间=i).first()
            db.session.delete(obj)
        db.session.commit()
        return jsonify({"code": 200, "msg": "success"})
    else:
        return jsonify({"code": 200, "msg": "error"})
    # else:
    #     return jsonify({"code": 403, "msg": "无权限"})
