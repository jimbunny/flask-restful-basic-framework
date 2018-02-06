#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by jim on 2018/1/30

from flask import Flask
APP_NAME = "flask-restful-api"
app = Flask(APP_NAME, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
print(app.config["HOST"])
# 现在通过app.config["VAR_NAME"]，我们可以访问到对应的变量


@app.route('/')
def hello_world():
    """

    :return:
    """
    return 'hello jim'


if __name__ == '__main__':
    # 读取配置文件配置
    host = app.config["HOST"]
    port = app.config["PORT"]
    debug = app.config["DEBUG"]
    app.run(host=host, port=port, debug=debug)
