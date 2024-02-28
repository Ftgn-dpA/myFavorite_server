import pymysql
from flask import Flask
from flask_cors import CORS

db = pymysql.connect(host='localhost', user='root', password='pp18001476164', database='myfavorite')
cursor = db.cursor()

app = Flask(__name__)
CORS(app, resources=r'/*')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899)
    db.close()
    print('end')
