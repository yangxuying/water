# -*- coding: utf-8 -*-
# @Time : 2019/10/28 15:49
# @Author : LangKai
# @Site : 
# @File : models.py
# @Software: PyCharm
from sqlalchemy import UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash

from . import db


class Base(db.Model):
    __abstract__ = True

    def to_json(self):
        dic = self.__dict__
        _dic = {}
        for i in dic:
            if i not in ['_sa_instance_state', 'password_hash', 'password']:
                _dic[i] = dic[i]
        return _dic

    def add_to_json(self, r):
        dic = [i.name for i in self.__table__.columns if i.name not in ['id']]
        for i in dic:
            setattr(self, i, r.get(i, None))
        return self

    def add_to_list(self, r):
        dic = [i.name for i in self.__table__.columns if i.name not in ['id']]
        data = dict(zip(dic, r))
        for i in dic:
            setattr(self, i, data.get(i, None))
        return self

    def get_matlab_data(self):
        dic = self.__dict__
        _dic = []
        for i in ['溶解氧', '高锰酸盐指数', '五日生化需氧量', '氨氮', '总磷']:  # 必须按照顺序
            _dic.append(dic[i])
        return _dic


class User(Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, comment="用户名")
    password_hash = db.Column(db.String(255), comment="密码哈希")
    ststus = db.Column(db.Boolean, default=True, comment="状态")
    avatar = db.Column(db.String(50), comment="头像")
    role = db.Column(db.String(50), comment="角色")

    def __repr__(self):
        return "<User_id:{0}>".format(self.id)

    @property
    def password(self):
        raise AttributeError("The password is not allowed to be read")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)


class Data(Base):
    __tablename__ = 'data'
    监测点 = db.Column(db.String(255), nullable=False, comment="水库名称")
    测量时间 = db.Column(db.String(255), nullable=False, comment="测量时间", primary_key=True)
    水温 = db.Column(db.Float, comment="水温")
    pH = db.Column(db.Float, comment="pH")
    溶解氧 = db.Column(db.Float, comment="溶解氧")
    电导率 = db.Column(db.Float, comment="电导率")
    浊度 = db.Column(db.Float, comment="浊度")
    高锰酸盐指数 = db.Column(db.Float, comment="高锰酸盐指数")
    总磷 = db.Column(db.Float, comment="总磷")
    总氮 = db.Column(db.Float, comment="总氮")
    叶绿素 = db.Column(db.Float, comment="叶绿素")
    蓝绿藻 = db.Column(db.Float, comment="蓝绿藻")
    氨氮 = db.Column(db.Float, comment="氨氮")


class YingData(Base):
    __tablename__ = 'YingData'
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True, comment="ID")
    断面名称 = db.Column(db.String(255), nullable=False, comment="断面名称")
    测量时间 = db.Column(db.String(255), nullable=False, comment="测量时间")
    溶解氧 = db.Column(db.Float, comment="溶解氧", nullable=False)
    高锰酸盐指数 = db.Column(db.Float, comment="高锰酸盐指数", nullable=False)
    五日生化需氧量 = db.Column(db.Float, comment="五日生化需氧量", nullable=False)
    氨氮 = db.Column(db.Float, comment="氨氮", nullable=False)
    总磷 = db.Column(db.Float, comment="总磷", nullable=False)
    FCM = db.Column(db.Float, comment="模糊聚类法")
    FCE = db.Column(db.Float, comment="模糊综合评价法")
    WQI = db.Column(db.Float, comment="水质综合指数法")
    SSO = db.Column(db.Float, comment="投影寻踪")

    __table_args__ = (
        UniqueConstraint('断面名称', '测量时间'),
    )

class GbData(Base):
    __tablename__ = 'GbData'
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True, comment="ID")
    溶解氧 = db.Column(db.Float, comment="溶解氧", nullable=False)
    高锰酸盐指数 = db.Column(db.Float, comment="高锰酸盐指数", nullable=False)
    五日生化需氧量 = db.Column(db.Float, comment="五日生化需氧量", nullable=False)
    氨氮 = db.Column(db.Float, comment="氨氮", nullable=False)
    总磷 = db.Column(db.Float, comment="总磷", nullable=False)
    等级 = db.Column(db.Float, comment="水质等级", nullable=False)
    类型 = db.Column(db.Float, comment="1,分级标准;2,最佳投影向量", nullable=False)
    is_use = db.Column(db.Float, comment="1,是;0,否", nullable=False)
