#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by jim on 2018/1/30

from flask import Flask
# from config import CONFIG

APP_NAME = "flask-restful-api"
app = Flask(APP_NAME, instance_relative_config=True)
app = Flask(APP_NAME)


def create_app():
    # app.config.from_object("config")
    # print app.config["HOST"]
    # 现在通过app.config["VAR_NAME"]，我们可以访问到对应的变量
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    app.secret_key = app.config['SECRET_KEY']
    # app.redis = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'],
    #                         db=app.config['REDIS_DB'], password=app.config['REDIS_PASSWORD'])
    #
    # app.q = Auth(access_key=app.config['QINIU_ACCESS_KEY'], secret_key=app.config['QINIU_SECRET_KEY'])
    # app.bucket_name = app.config['BUCKET_NAME']
    app.debug = app.config['DEBUG']
    from application import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')
    return app


if __name__ == '__main__':
    # 读取配置文件配置
    app = create_app()
    app.run(host="0.0.0.0", port=8888)
