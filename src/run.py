#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by jim on 2018/1/30

from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8888)
