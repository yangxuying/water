# -*- coding: utf-8 -*-
# @Time : 2019/10/28 15:50
# @Author : LangKai
# @Site : 
# @File : account.py
# @Software: PyCharm
import os
from flask import Blueprint, send_file, current_app, make_response
from flask import request

local_resource = Blueprint('local_resource', __name__)


def get_local_resource(data):
    file_name = data.args.get("document_save_name")
    document_name = data.args.get("document_name")
    file_path = os.path.join(current_app.config["UPLOAD_FILE_DIRS"], file_name)

    return send_file(file_path, attachment_filename=document_name, mimetype="application/octet-stream", as_attachment=True)


@local_resource.route('/local_resource', methods=['GET'])
def local_resource_():
    if request.method == "GET":
        res = get_local_resource(request)
        return res
