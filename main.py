from flask import Flask
from flask_cors import CORS
from users import users
from favorite import favorite
from dao import db

app = Flask(__name__)
CORS(app, resources=r'/*')

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(favorite, url_prefix='/favorite')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899)
    db.close()
    print('end')
