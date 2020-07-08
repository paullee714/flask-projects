import datetime
from pytz import timezone

from flask import Blueprint, request, jsonify

from model import my_user_model as my_user

user_route = Blueprint('user_route', __name__)


@user_route.route('/', methods=['GET'])
def main():
    return dict(msg='hello world!')


@user_route.route('/select/<name>', methods=['GET'])
def select_user(name):
    select_user = my_user.MyUser.query.filter_by(user_name=name).all()
    if len(select_user) == 0:
        return "user does not exists"
    else:
        select_user = select_user[0]
        return dict(id=select_user.id, name=select_user.user_name, created_at=select_user.created_at,
                    udpated_at=select_user.udpated_at)


@user_route.route('/select_all', methods=['GET'])
def select_all_user():
    select_user = my_user.MyUser.query.all()

    if len(select_user) == 0:
        return "user does not exists"
    else:
        user_list = []
        for user in select_user:
            data = dict(id=user.id, name=user.user_name, created_at=user.created_at, udpated_at=user.udpated_at)
            user_list.append(data)

        return jsonify(user_list)


@user_route.route('/insert', methods=['POST'])
def insert_user():
    packet = request.get_json()

    try:
        data = my_user.MyUser(
            user_name=packet.get('user_name'),
            created_at=datetime.datetime.now(timezone('Asia/Seoul')).replace(tzinfo=None),
            updated_at=datetime.datetime.now(timezone('Asia/Seoul')).replace(tzinfo=None)
        )

        select_user = my_user.MyUser.query.filter_by(user_name=packet.get('user_name')).all()

        if len(select_user) > 0:
            return "user is already exists"

        my_user.db.session.add(data)
        my_user.db.session.commit()
        my_user.db.session.remove()
        return "success!"
    except Exception as e:
        return "fail!"


@user_route.route('/update/<name>', methods=['POST'])
def update_user(name):
    select_user = my_user.MyUser.query.filter_by(user_name=name).all()
    if len(select_user) == 0:
        return "user does not exists"
    else:
        user = my_user.MyUser.query.filter_by(user_name=name).first()
        user.udpated_at = datetime.datetime.now(timezone('Asia/Seoul')).replace(tzinfo=None)
        my_user.db.session.commit()
        my_user.db.session.remove()
        return "update!"


@user_route.route('/delete/<name>', methods=['DELETE'])
def delete_user(name):
    select_user = my_user.MyUser.query.filter_by(user_name=name).all()
    if len(select_user) == 0:
        return "user does not exists"
    else:
        my_user.db.session.delete(select_user[0])
        my_user.db.session.commit()
        my_user.db.session.remove()
        return "delete user..."
