# Flask login - use session

Flask를 사용해서 사용자 login을 구현

# Flask Login

## Download & run Flask

```html
$ git clone https://github.com/paullee714/flask-projects.git
```

## Virtual Environments, Install Flask And Requirements module

```bash
$ virtualenv venv
$ source venv/bin/activate
(venv) $ install flask
$ pip install flask flask-sqlacodegen flask-SQLAlchemy pymysql
```

## Setup Database

```sql
create table flask_project.user_table(
    id int(5) not null auto_increment,
    user_name varchar(20) not null,
    password varchar(100) not null,
    bio varchar(256) default null,
    created_at datetime default current_timestamp,
    last_login datetime default null,
    PRIMARY KEY (id,user_name)
);
```

## Generate Flask ORM Model - sqlacodegen

```bash
$ flask-sqlacodegen "mysql+pymysql://root:qwerqwer123@localhost:3306/flask_project" --flask > user_model.py
# user_model.py 를 model 로 옮긴다.
```

```python
# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserTable(db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    user_name = db.Column(db.String(20, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    bio = db.Column(db.String(256, 'utf8mb4_unicode_ci'))
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    last_login = db.Column(db.DateTime)
```

## Setup Flask

```bash
.
├── README.md
├── __pycache__
│   └── app.cpython-37.pyc
├── app.py
├── model
│   ├── __init__.py
│   ├── __pycache__
│   └── user_model.py
├── route
│   ├── __init__.py
│   ├── __pycache__
│   ├── app_router.py
│   └── login_router.py
├── templates
│   ├── index.html
│   ├── login.html
│   └── register.html
└── user_table.sql
```

### app.py

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from route.login_router import login_route
from route.app_router import app_route

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:qwerqwer123@localhost:3306/flask_project"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy()
db.init_app(app)

app.register_blueprint(login_route)
app.register_blueprint(app_route)

app.secret_key = 'laksdjfoiawjewfansldkfnzcvjlzskdf'

if __name__ == '__main__':
    
    app.run(debug=True)
```

### route/app_router.py

```python
from flask import Blueprint, session, url_for, request, redirect,render_template

app_route = Blueprint('app_route',__name__)

@app_route.route('/',methods=['GET'])
def home():
    """
        Session Control
    """
    if session.get('name'):
        my_name = str(session['name'])
        r = "Hello User"
        return render_template('index.html',data=r)
    else:
        r = "hello Guest!"
        return render_template('index.html', data = r)
```

### route/login_router.py

```python
from flask import Blueprint, request, session, redirect, url_for, render_template

from model import user_model

login_route = Blueprint('login_route',__name__)

@login_route.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['user_name']
        password = request.form['password']
        try:
            data = user_model.UserTable.query.filter_by(user_name = name, password = password).first()
            if data is not None:
                session['name'] = True
                return redirect(url_for('app_route.home'))
            else:
                return render_template('login.html', data="user login fail!")
        except Exception as e:
            return "cannot login"

@login_route.route('/register/',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        new_user = user_model.UserTable(user_name = request.form['user_name'],password = request.form['password'])
        user_model.db.session.add(new_user)
        user_model.db.session.commit()
        return render_template('login.html')
    return render_template('register.html')

@login_route.route('/logout')
def logout():
    session['name'] = False
    return redirect(url_for('app_route.home'))
```

### model/user_model.py

```python
# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.schema import FetchedValue
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserTable(db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    user_name = db.Column(db.String(20, 'utf8mb4_unicode_ci'), primary_key=True, nullable=False, unique=True)
    password = db.Column(db.String(100, 'utf8mb4_unicode_ci'), nullable=False)
    bio = db.Column(db.String(256, 'utf8mb4_unicode_ci'))
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    last_login = db.Column(db.DateTime)
```

### templates/index.html

```html
<h1>
    index page
</h1>

{% if session['name'] %}
   
	{% if data %}
	<h3>{{data}}</h3>
	{% endif %}
	<a href="/logout">Logout</a> <br> <br>

{% else %}
<p>Not login!</p>

<a href="/login">Login</a> 
<a href="/register">Register</a>

{% endif %}
```

### templates/login.html

```html
<h1>
    login page
</h1>

<form action="/login" method="POST">
    <input type="username" name="user_name" placeholder="Username">
    <input type="password" name="password" placeholder="Password">
    <input type="submit" value="Log in">
</form>
{% if data %}
	<b>{{data}}</b>
{% endif %}
```

### templates/register.html

```html
<h1>
    register page
</h1>

<h2>Register</h2>
<form action="/register/" method="POST">
  <input type="username" name="user_name" placeholder="Username">
  <input type="password" name="password" placeholder="Password">
  <input type="submit" value="Log in">
</form>
```