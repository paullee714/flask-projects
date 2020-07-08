# Flask db연동 - CRUD

flask와 db연동을 합니다.

# Flask - Database(Mysql)

> DB - Mysql
Flask ORM Model From - SqlAlchemy

## Create DB & Table

DB 세팅 및 설치가 어렵다면, Docker를 사용해보자 

```sql
create table test_db.my_user(
	id int(11) NOT NULL auto_increment,
	user_name varchar(20),
	created_at datetime default current_timestamp,
	udpated_at datetime default current_timestamp,
	primary key(id)
);
```

## Create Flask App

> 간단한 테스트를 위해 REST API 형태로 CRUD를 작성 해 보겠습니다.

### Install, set, activate virtual environments

```bash
$ pip3 install virtualenv
$ mkdir flask-crud && cd flask-crud
$ virtualenv venv && source venv/bin/activate
(venv) $ pip3 install flask PyMySQL flask-sqlacodegen Flask-SQLAlchemy SQLAlchemy
```

### Configure Flask Structure

```bash
flask-crud
├── app.py
├── model
│   ├── __init__.py
│   ├── __pycache__
│   └── my_user_model.py
├── requirements.txt
├── route
│   ├── __init__.py
│   ├── __pycache__
│   └── user_route.py
└── venv
```

### app.py

```python
# flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# project module
from route.user_route import user_route

app = Flask(__name__)

##db info setting
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://wool:qwerqwer123@localhost:3306/test_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

## db set
db = SQLAlchemy()
db.init_app(app)

app.register_blueprint(user_route)

if __name__ == '__main__':
    
    app.run(debug=True)
```

### model/my_user_model.py

- sqlcodegen으로 data model을 생성해보자

```bash
$ flask-sqlacodegen "mysql+pymysql://wool:qwerqwer123@localhost:3306/test_db"  -- flask > my_user_model.py
# 생성된 my_user_model.py를 model로 옮기자
```

```python
# coding: utf-8
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MyUser(db.Model):
    """
        table name : my_user
        table info
            - id : index id
            - user name
            - created_at
            - updated_at
    """
    __tablename__ = 'my_user'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name = db.Column(db.String(20, 'utf8mb4_unicode_ci'))
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    udpated_at = db.Column(db.DateTime, server_default=db.FetchedValue())

    def __init__(self, user_name,created_at, updated_at):
        self.user_name = user_name
        self.created_at = created_at
        self.udpated_at = updated_at
```

### route/user_route.py

```python
import datetime
from pytz import timezone

from flask import Blueprint, request,jsonify

from model import my_user_model as my_user

user_route = Blueprint('user_route',__name__)

@user_route.route('/',methods=['GET'])
def main():
    return dict(msg='hello world!')

@user_route.route('/select/<name>',methods=['GET'])
def select_user(name):
    
    select_user = my_user.MyUser.query.filter_by(user_name=name).all()
    if len(select_user) == 0:
        return "user does not exists"
    else:
        select_user = select_user[0]
        return dict(id = select_user.id, name = select_user.user_name, created_at = select_user.created_at, udpated_at = user.udpated_at)

@user_route.route('/select_all',methods=['GET'])
def select_all_user():
    
    select_user = my_user.MyUser.query.all()
    
    if len(select_user) == 0:
        return "user does not exists"
    else:
        user_list = []
        for user in select_user:
            data = dict(id = user.id , name = user.user_name, created_at = user.created_at, udpated_at = user.udpated_at)
            user_list.append(data)
        
        return jsonify(user_list)

@user_route.route('/insert',methods=['POST'])
def insert_user():
    packet = request.get_json()

    try:
        data = my_user.MyUser(
            user_name = packet.get('user_name'),
            created_at = datetime.datetime.now(timezone('Asia/Seoul')).replace(tzinfo=None),
            updated_at = datetime.datetime.now(timezone('Asia/Seoul')).replace(tzinfo=None)
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
        
@user_route.route('/update/<name>',methods=['POST'])
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

@user_route.route('/delete/<name>',methods=['DELETE'])
def delete_user(name):
    select_user = my_user.MyUser.query.filter_by(user_name=name).all()
    if len(select_user) == 0:
        return "user does not exists"
    else:
        my_user.db.session.delete(select_user[0])
        my_user.db.session.commit()
        my_user.db.session.remove()
        return "delete user..."
```

## TEST API

### Run Server

```bash
(venv) $ python app.py
```

### Request

간단히 터미널에서 curl 명령어로 테스트 가능

```bash
$ curl -X GET localhost:5000/
```

Postman 을 사용해서 테스트했다

> method - GET
test url : localhost:5000/select/wool

- wool 의 자리에 user name을 입력하면 된다

> method - GET
test url : localhost:5000/select_all

> method - POST
test url : localhost:5000/insert

- body

    {
    "user_name":"tom"
    }

> method - DELETE
test url : localhost:5000/delete/wool

- delete 할 username을 wool 대신 입력 → 해당 사용자 삭제

> method - UPDATE
test url : localhost:5000/update/wool

- update 할 username을 wool 대신 입력 → update_at이 현재시간으로 변경