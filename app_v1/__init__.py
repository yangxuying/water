# -*- coding: utf-8 -*-
import os
from flask import Flask
from flask_redis import FlaskRedis
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # 实例化
sess = Session()
redis_client = FlaskRedis()
from .views import local_resource, User, userManagement, dateManagement, yingManagement


def init_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static', static_url_path='/static')
    # 适配gunicorn部署生产环境
    app.config.from_object('settings.{}'.format(os.environ.get('FLASK_SETTING', 'Development')))
    # 将db注册到app中
    db.init_app(app)
    sess.init_app(app)
    redis_client.init_app(app)
    # 注册蓝图
    app.register_blueprint(User.user, url_prefix="/vab-flask-server")
    app.register_blueprint(userManagement.api, url_prefix="/vab-flask-server/userManagement")
    app.register_blueprint(dateManagement.api, url_prefix="/vab-flask-server/dateManagement")
    app.register_blueprint(local_resource.local_resource, url_prefix="/vab-flask-server")
    app.register_blueprint(yingManagement.api, url_prefix="/vab-flask-server/yingManagement")
    return app
