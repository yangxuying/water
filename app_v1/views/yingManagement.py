from flask import Blueprint, session
from flask import request
from flask.json import jsonify
from sqlalchemy import and_
import pandas as pd

from utils.ying.runMatlab import runQualityAnalysis

from .. import db
from .. import models

api = Blueprint('YingData', __name__)


@api.route('/', methods=['GET'])
def YingManagement():
    """
    swagger_from_file: ./swagger_apis/YingManagement/YingManagement.yml
    :return:
    """
    return jsonify({"code": 200, "data": [], "msg": "success"})


@api.route("getList", methods=['POST'])
def YingManagement_getList():
    """
        swagger_from_file: ./swagger_apis/YingManagement/YingManagement_getList.yml
        :return:
    """

    res = dict()

    # if session.get('role'):
    try:
        table = getattr(models, api.name)
        pageNo = request.json.get('pageNo') if request.json.get('pageNo') else 1
        pageSize = request.json.get('pageSize') if request.json.get('pageSize') else 10
        kwargs = dict()
        if request.json.get('name'):
            kwargs.update({'断面名称': request.json.get('name')})
        if request.json.get('date'):
            kwargs.update({'测量时间': request.json.get('date')})
        totalCount = db.session.query(table.断面名称).filter_by(**kwargs).count()
        data = db.session.query(table).filter_by(**kwargs).order_by(table.断面名称).offset(
            (pageNo - 1) * pageSize).limit(pageSize).all()
        res.update({'code': 200, 'pageNo': pageNo, 'pageSize': pageSize, 'totalCount': totalCount,
                    'data': [i.to_json() for i in data], 'msg': 'success'})
    except Exception as e:
        res.update({'code': 500, 'data': [], 'msg': str(e)})
    # else:
    #     res.update({"code": 403, "msg": "无权限"})

    return jsonify(res)


@api.route("getNames", methods=['GET'])
def YingManagement_getNames():
    """
        swagger_from_file: ./swagger_apis/YingManagement/YingManagement_getNames.yml
        :return:
    """

    res = dict()

    # if session.get('role'):
    try:
        table = getattr(models, api.name)
        data = db.session.query(table.断面名称).group_by(table.断面名称).all()

        data_list = []

        for i in range(0, len(data)):
            sur_time = db.session.query(table.测量时间).filter(table.断面名称 == data[i][0]).all()

            children = []
            for n in range(1, len(sur_time)):
                children.append({"id": '{}-{}'.format(i, n), "label": sur_time[n][0]})

            var = {"id": i, "label": data[i][0], "children": children}

            data_list.append(var)

        res.update({'code': 200, 'data': data_list, 'msg': 'success'})
    except Exception as e:
        res.update({'code': 500, 'data': [], 'msg': str(e)})
    # else:
    #     res.update({"code": 403, 'data': [], "msg": "无权限"})

    return jsonify(res)


@api.route("getOperations", methods=['GET'])
def YingManagement_getOperations():
    """
        swagger_from_file: ./swagger_apis/YingManagement/YingManagement_getOperations.yml
        :return:
    """

    res = dict()

    # if session.get('role'):
    try:
        data = {'模糊聚类法': 'FCM', '模糊综合评价法': 'FCE', '水质综合指数法': 'WQI', '投影寻踪法': 'SSO'}
        res.update({'code': 200, 'data': data, 'msg': 'success'})
    except Exception as e:
        res.update({'code': 500, 'data': [], 'msg': str(e)})
    # else:
    #     res.update({"code": 403, 'data': [], "msg": "无权限"})

    return jsonify(res)


@api.route("doEdit", methods=['POST'])
def YingManagement_doEdit():
    """
        swagger_from_file: ./swagger_apis/YingManagement/YingManagement_doEdit.yml
        :return:
    """

    res = dict()

    # if session.get('role'):
    try:
        if request.json.get('id'):
            request.json.pop('id')
        table = getattr(models, api.name)
        name = request.json.get('name')
        date = request.json.get('date')
        if name and date:
            kwargs = dict()
            kwargs.update({'断面名称': name, '测量时间': date})
            data = db.session.query(table).filter_by(**kwargs).first()
            if data:
                data.add_to_json(request.json)
                db.session.commit()
                res.update({"code": 200, 'data': [], "msg": "success"})
            else:
                raise Exception('数据不存在')
        else:
            raise Exception('断面名称和测量时间必填')
    except Exception as e:
        res.update({'code': 500, 'data': [], 'msg': str(e)})
    # else:
    #     res.update({"code": 403, "msg": "无权限"})

    return jsonify(res)


@api.route("doDelete", methods=['POST'])
def YingManagement_doDelete():
    """
        swagger_from_file: ./swagger_apis/YingManagement/YingManagement_doDelete.yml
        :return:
    """
    res = dict()

    # if session.get('role'):
    try:
        table = getattr(models, api.name)
        name = request.json.get('name')
        date = request.json.get('date')
        if name and date:
            kwargs = dict()
            kwargs.update({'断面名称': name, '测量时间': date})
            data = db.session.query(table).filter_by(**kwargs).first()
            if data:
                db.session.delete(data)
                db.session.commit()
                res.update({"code": 200, 'data': [], "msg": "success"})
            else:
                raise Exception('数据不存在')
        else:
            raise Exception('断面名称和测量时间必填')
    except Exception as e:
        res.update({'code': 500, 'data': [], 'msg': str(e)})
    # else:
    #     res.update({"code": 403, "msg": "无权限"})

    return jsonify(res)


@api.route("doNew", methods=['POST'])
def YingManagement_doNew():
    """
        swagger_from_file: ./swagger_apis/YingManagement/YingManagement_doNew.yml
        :return:
    """
    res = dict()

    # if session.get('role'):
    try:
        table = getattr(models, api.name)
        if request.json.get('id'):
            request.json.pop('id')
        name = request.json.get('name')
        date = request.json.get('date')
        if name and date:
            kwargs = dict()
            kwargs.update({'断面名称': name, '测量时间': date})
            data = db.session.query(table).filter_by(**kwargs).first()
            if not data:
                new_data = table()
                new_data.add_to_json(request.json)
                db.session.add(new_data)
                db.session.commit()
                res.update({"code": 200, 'data': [], "msg": "success"})
            else:
                raise Exception('数据已存在')
        else:
            raise Exception('断面名称和测量时间必填')
    except Exception as e:
        res.update({'code': 500, 'data': [], 'msg': str(e)})
    # else:
    #     res.update({"code": 403, "msg": "无权限"})

    return jsonify(res)


@api.route("uploadFile", methods=['POST'])
def YingManagement_uploadFile():
    """
        swagger_from_file: ./swagger_apis/YingManagement/YingManagement_doNew.yml
        :return:
    """
    res = dict()

    # if session.get('role'):
    table = getattr(models, api.name)
    file = request.files.get('file')
    data = pd.read_excel(file).to_dict('list')

    # 检查excel格式和获取excel数据
    try:
        if data.get('断面名称') is None:
            raise Exception('未找到断面名称列')
        name_list = [i if not pd.isna(i) else None for i in data.get('断面名称')]
        while None in name_list:
            name_list.remove(None)

        if data.get('年') is None:
            raise Exception('未找到测量时间列')
        year_list = [i if not pd.isna(i) else None for i in data.get('年')]
        while None in year_list:
            year_list.remove(None)

        if data.get('月') is None:
            raise Exception('未找到测量时间列')
        month_list = [i if not pd.isna(i) else None for i in data.get('月')]
        while None in month_list:
            month_list.remove(None)

        if data.get('溶解氧(mg/l)') is None:
            raise Exception('未找到溶解氧列')
        o2_list = [i if not pd.isna(i) else None for i in data.get('溶解氧(mg/l)')]
        while None in o2_list:
            o2_list.remove(None)

        if data.get('高锰酸盐指数(mg/l)') is None:
            raise Exception('未找到高锰酸盐指数列')
        km_list = [i if not pd.isna(i) else None for i in data.get('高锰酸盐指数(mg/l)')]
        while None in km_list:
            km_list.remove(None)

        if data.get('五日生化需氧量(mg/l)') is None:
            raise Exception('未找到五日生化需氧量列')
        d5_list = [i if not pd.isna(i) else None for i in data.get('五日生化需氧量(mg/l)')]
        while None in d5_list:
            d5_list.remove(None)

        if data.get('氨氮(mg/l)') is None:
            raise Exception('未找到氨氮列')
        nh_list = [i if not pd.isna(i) else None for i in data.get('氨氮(mg/l)')]
        while None in nh_list:
            nh_list.remove(None)

        if data.get('总磷(mg/l)') is None:
            raise Exception('未找到总磷列')
        p_list = [i if not pd.isna(i) else None for i in data.get('总磷(mg/l)')]
        while None in p_list:
            p_list.remove(None)
    except Exception as e:
        res.update({'code': 500, 'data': [], 'msg': str(e)})
        return jsonify(res)

    try:
        # 格式化测量时间
        date_list = list()
        for year, month in zip(year_list, month_list):
            year = str(int(year))
            month = str(int(month) if month >= 10 else '0{}'.format(int(month)))
            date_list.append('{}-{}'.format(year, month))

        # 断面名称, 测量时间, 溶解氧, 高锰酸盐指数, 五日生化需氧量, 氨氮, 总磷

        data = list(zip(name_list, date_list, o2_list, km_list, d5_list, nh_list, p_list))

        # 插入数据到数据库
        success = 0
        err = 0
        skip = 0
        try:
            for i in data:
                name = i[0]
                date = i[1]
                if name and date:
                    kwargs = dict()
                    kwargs.update({'断面名称': name, '测量时间': date})
                    is_have = db.session.query(table).filter_by(**kwargs).first()
                    if not is_have:
                        new_data = table()
                        new_data.add_to_list(i)
                        db.session.add(new_data)
                        db.session.commit()
                        success += 1
                    else:
                        skip += 1
                else:
                    raise Exception('断面名称和测量时间必填')
        except:
            err += 1

        res.update({'code': 200, 'data': {'success': success, 'err': err, 'skip': skip}, 'msg': 'success'})
    except Exception as e:
        res.update({'code': 500, 'data': [], 'msg': str(e)})
    # else:
    #     res.update({"code": 403, "msg": "无权限"})

    return jsonify(res)


@api.route("doRun", methods=['POST'])
def YingManagement_doRun():
    """
        swagger_from_file: ./swagger_apis/YingManagement/YingManagement_doRun.yml
        :return:
    """
    res = dict()

    # if session.get('role'):
    try:
        table = getattr(models, api.name)
        name = request.json.get('name')
        start = request.json.get('start')
        end = request.json.get('end')
        operation = request.json.get('operation')
        kwargs = dict()
        # Select data by condition
        if name:
            kwargs.update({'断面名称': name})
        if start and end and operation != 'FCM':
            import datetime
            if not datetime.datetime.strptime(start, '%Y-%m') < datetime.datetime.strptime(end, '%Y-%m'):
                start, end = end, start
            data = db.session.query(table).filter_by(**kwargs).filter(
                and_(table.测量时间 >= start, table.测量时间 < end)).all()
        else:
            data = db.session.query(table).filter_by(**kwargs).all()
        if operation == 'SSO':
            # insert gb data
            data_gb = db.session.query(models.GbData).filter(models.GbData.类型 == 1).all()
            for gb in data_gb:
                data.append(gb)
        # Do run matlab
        matlab_res = runQualityAnalysis([i.get_matlab_data() for i in data], operation)
        # Update data from matlab_res
        if matlab_res is not None:
            for db_obj, level in zip(data, matlab_res):
                setattr(db_obj, operation, level)
            db.session.commit()
        else:
            raise Exception('计算方式错误')
        res.update({"code": 200, 'data': [], "msg": "success"})
    except Exception as e:
        res.update({'code': 500, 'data': [], 'msg': str(e)})
    # else:
    #     res.update({"code": 403, "msg": "无权限"})

    return jsonify(res)
