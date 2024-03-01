from dao import db, cursor
from flask import request, jsonify
from flask import Blueprint

users = Blueprint('users', __name__)


@users.route('/list', methods=['GET'])
def user_list():
    """
    列举系统的所有用户
    :return:
        json键值对
    """
    if request.method == 'GET':
        cursor.execute('SELECT id, username, role, create_time FROM users')
        data = cursor.fetchall()
        return jsonify([{'id': i[0], 'username': i[1], 'role': i[2], 'create_time': i[3]} for i in data])


@users.route('/register', methods=['POST'])
def user_register():
    """
    注册新用户
        username 用户名
        password 密码
    用户身份（role）
        0：超级管理员
        1：普通管理员
        2：普通用户（默认）
    :return:
        0 注册成功
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        cursor.execute(f'INSERT INTO users VALUES (NULL, "{username}", "{password}", "{role}", CURRENT_TIMESTAMP)')
        db.commit()
        return '0'


@users.route('/login', methods=['POST'])
def user_login():
    """
    用户登录验证
        username 用户名
        password 密码
    :return:

    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cursor.execute(f'SELECT id, username, role FROM users WHERE username="{username}" AND password="{password}"')
        data = cursor.fetchone()
        if data is None:
            return jsonify({})
        else:
            return jsonify({'id': data[0], 'username': data[1], 'role': data[2]})


@users.route('/alt_password', methods=['POST'])
def user_alt_password():
    """
    修改密码
        user_id 用户id
        old_password 旧密码
        new_password 新密码
    :return:
        0 正常
        1 旧密码错误
    """
    if request.method == 'POST':
        user_id = request.form.get('id')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        cursor.execute(f'SELECT password FROM users WHERE id="{user_id}"')
        if old_password != cursor.fetchone()[0]:
            return '1'
        else:
            cursor.execute(f'UPDATE users SET password="{new_password}" WHERE id="{user_id}"')
            db.commit()
            return '0'


@users.route('/alt_role', methods=['POST'])
def user_alt_role():
    """

    :return:
    """
    if request.method == 'POST':
        uid = request.form.get('uid')
        role = request.form.get('role')
        cursor.execute(f'UPDATE users SET role="{role}" WHERE id="{uid}"')
        db.commit()
        return '0'


@users.route('/del', methods=['POST'])
def user_del():
    """
    删除用户
        uid 要删除的目标用户id
    :return:
        0 正常
        1 SQL错误
    """
    if request.method == 'POST':
        uid = request.form.get('uid')
        try:
            cursor.execute(f'DELETE FROM users WHERE id="{uid}"')
            cursor.execute(f'DELETE FROM favorite WHERE owner="{uid}"')
            db.commit()
            return '0'
        except Exception as e:
            db.rollback()
            print(e)
            return '1'


@users.route('/view', methods=['GET'])
def favorite_view():
    """

    :return:
    """
    if request.method == 'GET':
        owner = request.args.get('owner')
        cursor.execute(f'SELECT name, url, description FROM favorite WHERE owner="{owner}" AND visibility=1')
        data = cursor.fetchall()
        return jsonify([{'name': i[0], 'url': i[1], 'description': i[2]} for i in data])
