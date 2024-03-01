from dao import db, cursor
from flask import request, jsonify
from flask import Blueprint

favorite = Blueprint('favorite', __name__)


@favorite.route('/list', methods=['GET'])
def favorite_list():
    """
    列举当前用户所有收藏网站信息
    :return:
        json键值对
    """
    if request.method == 'GET':
        owner = request.args.get('owner')
        cursor.execute(f'SELECT fid, name, url, visibility, description FROM favorite WHERE owner="{owner}"')
        data = cursor.fetchall()
        return jsonify([{'fid': i[0], 'name': i[1], 'url': i[2], 'visibility': i[3], 'description': i[4]} for i in data])


@favorite.route('/add', methods=['POST'])
def favorite_add():
    """
    添加收藏网站
    :return:
    """
    if request.method == 'POST':
        name = request.form.get('name')
        url = request.form.get('url')
        owner = request.form.get('owner')
        visibility = request.form.get('visibility')
        description = request.form.get('description')
        cursor.execute(f'INSERT INTO favorite VALUES (NULL, "{name}", "{url}", "{owner}", "{visibility}", "{description}")')
        db.commit()
        return '0'


@favorite.route('/del', methods=['POST'])
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


@favorite.route('/update', methods=['POST'])
def favorite_update():
    """

    :return:
    """
    if request.method == 'POST':
        fid = request.form.get('fid')
        new_name = request.form.get('new_name')
        new_url = request.form.get('new_url')
        new_visibility = request.form.get('new_visibility')
        new_description = request.form.get('new_description')
        cursor.execute(f'UPDATE favorite SET name="{new_name}", url="{new_url}",visibility="{new_visibility}", description="{new_description}" WHERE fid="{fid}"')
        db.commit()
        return '0'
