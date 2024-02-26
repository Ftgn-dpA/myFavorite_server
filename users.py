import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS

db = pymysql.connect(host='localhost', user='root', password='pp18001476164', database='myfavorite')
cursor = db.cursor()

app = Flask(__name__)
CORS(app, resources=r'/*')


@app.route('/users/list', methods=['GET'])
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


@app.route('/users/register', methods=['POST'])
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


@app.route('/users/login', methods=['POST'])
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


@app.route('/users/alt_password', methods=['POST'])
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


@app.route('/users/alt_role', methods=['POST'])
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


@app.route('/users/del', methods=['POST'])
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


@app.route('/favorite/list', methods=['GET'])
def favorite_list():
    """
    列举当前用户所有收藏网站
    :return:
        json键值对
    """
    if request.method == 'GET':
        owner = request.args.get('owner')
        cursor.execute(f'SELECT fid, name, description, url FROM favorite WHERE owner="{owner}"')
        data = cursor.fetchall()
        return jsonify([{'fid': i[0], 'name': i[1], 'description': i[2], 'url': i[3]} for i in data])


@app.route('/favorite/add', methods=['POST'])
def favorite_add():
    """
    添加收藏网站
    :return:
    """
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        owner = request.form.get('owner')
        description = request.form.get('description')
        cursor.execute(f'INSERT INTO favorite VALUES (NULL, "{name}", "{url}", "{owner}", "{description}")')
        db.commit()
        return '0'


@app.route('/favorite/del', methods=['POST'])
def favorite_del():
    """

    :return:
    """
    if request.method == 'POST':
        print(request.form)
        fid = request.form.get('fid')
        cursor.execute(f'DELETE FROM favorite WHERE fid="{fid}"')
        db.commit()
        return '0'


@app.route('/favorite/update', methods=['POST'])
def favorite_update():
    """

    :return:
    """
    if request.method == 'POST':
        fid = request.form.get('fid')
        new_name = request.form.get('new_name')
        new_url = request.form.get('new_url')
        new_description = request.form.get('new_description')
        cursor.execute(f'UPDATE favorite SET name="{new_name}", url="{new_url}", description="{new_description}" WHERE fid="{fid}"')
        db.commit()
        return '0'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899)
    db.close()
    print('end')
