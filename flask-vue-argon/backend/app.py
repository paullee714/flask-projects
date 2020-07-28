from flask import Flask, jsonify, request,session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt

from my_util.my_logger import my_logger
from my_provider.baseball_scrapper import get_baseball_rank
from my_model.user_model import User

import os,string
import json

# instantiate the app
app = Flask(__name__)
app.secret_key = 'laksdjfoiawjewfansldkfnzcvjlzskdf'

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
db = SQLAlchemy()
db.init_app(app)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

bcrypt = Bcrypt(app)

# sanity check route
@app.route('/', methods=['GET'])
def test_router():
    my_logger.info("hello this is root url!")
    return jsonify('This is Docker Test developments Server!')


@app.route('/health_check', methods=['GET'])
def health_check():
    my_logger.info("health check route url!")
    return jsonify('good')

@app.route('/main_btn',methods=['GET'])
def main_btn():
    my_logger.info("click Main Btn")
    data = []
    string_pool = string.ascii_lowercase
    result_dict={}

    for i in range(15):
        result_val=''

        for i in range(10):
            import random
            result_val += random.choice(string_pool)

        result_dict['key'] = result_val

        data.append(result_dict)

    return jsonify(data)


@app.route('/baseball_data',methods=['GET'])
def new_data():
    my_logger.info("baseball_data route!")
    data_list = get_baseball_rank()
    return jsonify(data_list)


@app.route("/api/auth/login",methods=['POST'])
def auth_login():
    my_logger.info("User auth Login")
    my_logger.info(request.get_json())

    username = request.get_json().get('username')
    useremail = request.get_json().get('useremail')
    userpwd = request.get_json().get('userpwd')
    bio = request.get_json().get('bio')

    try:
        user_data = User.query.filter_by(username=username,userpwd=userpwd).first()
        if user_data is not None:
            my_logger.info("login success!")
            session['name'] = True
            return {'success':'user Login Success!'}
        else:
            my_logger.info("user does not exists....")
            session['name'] = False
            return {'success':'user does not exists.....'}
    except Exception as e:
        my_logger.error(e)
        session['login_session'] = False
        return {'error':'login Exception...'}


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=os.getenv('FLASK_RUN_PORT'),debug=os.getenv('FLASK_DEBUG'))
