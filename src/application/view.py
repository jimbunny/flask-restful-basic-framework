# coding:utf-8
from flask import Flask, request, jsonify
from model import User, db_session
import hashlib
import time
import redis

app = Flask(__name__)
redis_store = redis.Redis(host='localhost', port=6379, db=4, password='')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['POST'])
def login():
    phone_number = request.get_json().get('phone_number')
    password = request.get_json().get('password')
    user = User.query.filter_by(phone_number=phone_number).first()
    if not user:
        return jsonify({'code': 0, 'message': '没有此用户'})

    if user.password != password:
        return jsonify({'code': 0, 'message': '密码错误'})

    m = hashlib.md5()
    m.update(phone_number)
    m.update(password)
    m.update(str(int(time.time())))
    token = m.hexdigest()

    redis_store.hmset('user:%s' % user.phone_number, {'token': token, 'nickname': user.nickname, 'app_online': 1})
    redis_store.set('token:%s' % token, user.phone_number)
    redis_store.expire('token:%s' % token, 3600*24*30)

    return jsonify({'code': 1, 'message': '成功登录', 'nickname': user.nickname, 'token': token})


@app.route('/user')
def user():
    token = request.headers.get('token')
    if not token:
        return jsonify({'code': 0, 'message': '需要验证'})
    phone_number = redis_store.get('token:%s' % token)
    if not phone_number or token != redis_store.hget('user:%s' % phone_number, 'token'):
        return jsonify({'code': 2, 'message': '验证信息错误'})

    nickname = redis_store.hget('user:%s' % phone_number, 'nickname')
    return jsonify({'code': 1, 'nickname': nickname, 'phone_number': phone_number})


@app.route('/logout')
def logout():
    token = request.headers.get('token')
    if not token:
        return jsonify({'code': 0, 'message': '需要验证'})
    phone_number = redis_store.get('token:%s' % token)
    if not phone_number or token != redis_store.hget('user:%s' % phone_number, 'token'):
        return jsonify({'code': 2, 'message': '验证信息错误'})

    redis_store.delete('token:%s' % token)
    redis_store.hmset('user:%s' % phone_number, {'app_online': 0})
    return jsonify({'code': 1, 'message': '成功注销'})


@app.teardown_request
def handle_teardown_request(exception):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5007)
