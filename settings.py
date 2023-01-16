# -*- coding: utf-8 -*-


from app_v1 import db
import pymysql


class Base(object):
    # redis
    REDIS_URL = "redis://82.157.232.247:6379/0"
    # REDIS_URL = "redis://localhost:6379/0"
    # session配置
    # SESSION_TYPE = 'redis'  # session类型为redis
    # SESSION_KEY_PREFIX = 'session:'  # 保存到session中的值的前缀
    # SESSION_PERMANENT = False  # 如果设置为False，则关闭浏览器session就失效。
    # SESSION_USE_SIGNER = False  # 是否对发送到浏览器上 session:cookie值进行加密
    # SESSION_REDIS = redis.Redis(host='localhost', port='6379')
    SECRET_KEY = '123456'
    SESSION_TYPE = 'sqlalchemy'  # session类型为sqlalchemy
    SESSION_SQLALCHEMY = db  # SQLAlchemy对象
    SESSION_SQLALCHEMY_TABLE = 'session'  # session要保存的表名称
    SESSION_PERMANENT = True  # 如果设置为True，则关闭浏览器session就失效。
    SESSION_USE_SIGNER = False  # 是否对发送到浏览器上session的cookie值进行加密
    SESSION_KEY_PREFIX = 'session:'  # 保存到session中的值的前缀
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:Xujc123..@82.157.232.247:3306/water"
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost:3306/water"
    # SQLALCHEMY_DATABASE_URI = r'sqlite:///D:\PycharmProjects\111\foo.db'
    SQLALCHEMY_POOL_SIZE = 5  # 数据库连接池的大小。默认值 5
    SQLALCHEMY_POOL_TIMEOUT = 30  # 指定数据库连接池的超时时间。默认是 10
    SQLALCHEMY_POOL_RECYCLE = -1
    SQLALCHEMY_MAX_OVERFLOW = 3  # 控制在连接池达到最大值后可以创建的连接数。当这些额外的连接回收到连接池后将会被断开和抛弃
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 追踪对象的修改并且发送信号
    # SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    UPLOAD_FILE_DIRS = r"D:\PycharmProjects\3ta037\static\video"
    JSON_AS_ASCII = False
    JSONIFY_MIMETYPE = "application/json;charset=utf-8"


class Production(Base):
    """生产配置文件"""
    SERVER_NAME = '82.157.232.247:80'
    ENV = 'Production'
    DEBUG = False


class Development(Base):
    """开发配置文件"""
    # SERVER_NAME = '192.168.1.2:5001'
    SERVER_NAME = '127.0.0.1:5001'
    ENV = 'Development'
    DEBUG = True


class Testing(Base):
    """
    测试配置文件
    """
    pass
