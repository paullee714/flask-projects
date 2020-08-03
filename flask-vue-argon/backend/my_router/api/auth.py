"""
@oliver
url route split
"""
from flask import Blueprint, request, jsonify, current_app
from my_util.my_logger import my_logger
from my_model import user_model

import jwt
import datetime

auth_route = Blueprint('auth_route', __name__)


@auth_route.route('/logout', methods=['POST'])
def logout():
    return jsonify("hi!")


@auth_route.route('/get_user', methods=['GET'])
def get_login_user():
    return jsonify("hi!")


@auth_route.route('/signup', methods=['POST'])
def user_register():
    # 로그
    my_logger.info("user register")
    data = request.get_json()
    db = user_model.db

    user_data = user_model.User.query.filter_by(username=data.get('username')).first()
    if user_data is not None:
        my_logger.error("Username is Already exist")
        return {"success": "username is already exist"}

    user = user_model.User(**data)
    user.has_password()
    db.session.add(user)
    db.session.commit()

    my_logger.info("user Save Success")

    return jsonify(user.to_dict()), 200


@auth_route.route('/login', methods=['POST'])
def login():
    my_logger.info("User Login")

    data = request.get_json()
    user_data = user_model.User.query.filter_by(username=data.get('username')).first()

    if user_data is not None:
        auth = user_data.check_password(data.get("userpwd"))

        if not auth:
            my_logger.error("Authentication valid error")
            return jsonify({'message': 'Authentication valid error', "authenticated": False}), 401

        my_logger.info("User Authentication token setting")
        token = jwt.encode({
            'sub': user_data.username,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, 'qwersdaiofjhoqwihlzxcjvjl')

        my_logger.info("Set up Success")
        my_logger.debug(token.decode('UTF-8'))
        return jsonify({"token": token.decode('UTF-8')})
    else:
        my_logger.error("User Does Not Exist")
        return jsonify({'message': 'User Does Not Exist', "authenticated": False}), 401
