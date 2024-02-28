from main import *
from flask import request, jsonify


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
