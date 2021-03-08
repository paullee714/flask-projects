# Flask 스마트한 구조 만들기
- 블로그 링크 Link [https://woolbro.tistory.com/120]

# Flask 스마트하게 구조 만들기!

- 전에는 Spring, Django를 사용해서 프로젝트를 구축했다. 개발을 시작하기 전에 세팅 해야 할 것, 그리고 환경설정과 지원하는 서비스의 파악 등, 실제로 작업을 하는데 까지 걸리는 시간이 오래 걸렸다.
- 플라스크는 미니멀하게 프로젝트를 시작 할 수 있어서, 초기 진입 시에 세팅과 공부 할 것들이  비교적 적은 편이라고 생각했다.
- 플라스크로 현업에서, 그리고 사이드 프로젝트로 개발을 진행 하다 보니 미니멀하게 금방 작업 하는 것에는 도움이 되었지만, Django나  Spring처럼 구조화를 하기는 조금 어렵다는 생각이 들었다.
- '나만의 플라스크 스트럭쳐 구성'을 만들어 놓고 작업을 해 놓으면 좋겠다! 라는 생각이 들어 정리하려고한다.

## 가상환경

- 호불호에 따라, 그리고 여론에 따라서 pipenv, virtualenv 로 나뉜다고 알고있다.
- 주로 virtualenv를 사용했었지만, pipenv를 사용해 보고 싶다는 생각이 들었다. 뭔가 좀 더 직관적인 느낌이다.

### install pipenv

`pipenv`를 사용하면 `pip freeze`으로 남겨주었던 `requirements.txt`를 남기지 않고도 **`pipfile`**으로 자동으로 남는다. 너무 편하다.

```bash
$ pip3 install pipenv # 설치가 되어있지 않다면!
$ pipenv shell # <-- 가상환경을 자동으로 만들어주고, 실행시켜준다.
(가상환경이름) $ pipenv install [package_name] # <-- 가상환경 내에 설치
```

### 내가 설치 한 요소들 - Pipfile

설치를 하면, 같은 경로 내의 Pipfile로 저장이 된다.

내가 설치한 명령어와 Pipfile이다

```bash
(가상환경이름) $ pipenv install flask flask-script python-dotenv
```

```bash
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
flask = "*"
flask-script = "*"
python-dotenv = "*"

[dev-packages]
autopep8 = "*"

[requires]
python_version = "3.9"
```

## 파일 구조

- 매 프로젝트마다 이렇게 하지는 않지만, 크게 아래와 같이 잡고있다.
- 더불어서 여러가지 고민이 있다.
    - app패키지 내에 router와 provider들을 넣어주는 방법
    - app패키지 내에 각  도메인별로 폴더를 나누어 각각 router, provider를 만드는 법
    - 그냥 app.py와 route, provider 들을 만드는 방법.

### 구조

```bash
.
├── Pipfile
├── Pipfile.lock
├── README.md
├── app
│   └── __init__.py
├── config
│   ├── __init__.py
│   └── flask_config.py
├── manage.py
├── model
│   ├── __init__.py
│   └── test_model.py
├── provider
│   ├── __init__.py
│   ├── common_provider.py
│   ├── first
│   │   ├── __init__.py
│   │   └── first_provider.py
│   └── second
│       ├── __init__.py
│       └── second_provider.py
└── router
    ├── __init__.py
    ├── first_router
    │   ├── __init__.py
    │   └── first.py
    └── second_router
        ├── __init__.py
        └── second.py
```

- app/__init__.py : 플라스크 APP 전체의 구조와 설정들을 주입 해 주는 곳이다.
- config/flask_config.py : 플라스크의 환경설정 주입을 관장한다. app/__init__.py에서 환경 변수를 주입 하기 전에 `.env(dot-env)`로 환경을 파악 해서 production과 develop 환경을 구분 해 준다.
- model : 데이터베이스 모델 (ORM)이 있는 곳 (여기서는 작성하지 않았다)
- provider : 각 api의 endpoint에서 사용 할 '서비스'의 영역을 작업 한다.
- router : 각  api의 endpoint를 정해준다. 정말 말 그대로 "ROUTE"만 해 주는것이 목표이다. 최대한 깔끔하게.

## 각 패키지를 뜯어볼까

- 각 패키지들 중에 내가 중요하게 생각해서 분리 한 것들을 위주로 적어 보았다.
- 여기서 직접 작성하지 않은 패키지/모듈 들은 간단하게 설명하고 넘어가려고 한다.

### app/__init__.py

```python
from flask import Flask, jsonify
from config import flask_config
from router import first_router

def register_router(flask_app: Flask):
    # router들을 등록 해주는 곳
    from router.first_router.first import first
    from router.second_router.second import second

    flask_app.register_blueprint(first)
    flask_app.register_blueprint(second)

    # flask app의 request/response들과 매번 함께 실행 할 함수 정의
    @flask_app.before_request
    def before_my_request():
        print("before my request")

    @flask_app.after_request
    def after_my_request(res):
        print("after my request", res.status_code)
        return res

def create_app():
    # 앱 설정
    app = Flask(__name__)
    app.config.from_object((get_flask_env()))
    register_router(app)
    return app

def get_flask_env():
    # 환경변수에 따라 config나누기
    if(flask_config.Config.ENV == "prod"):
        return 'config.flask_config.prodConfig'
    elif (flask_config.Config.ENV == "dev"):
        return 'config.flask_config.devConfig'
```

- register_router(flask_app: Flask) - Flask를 매개변수로 받는 함수를 만들어, blueprint들을 관리한다. 각각 분리한 router들을 등록하는 작업들을 해주었고,  서버에 들어온 request를 처리하기 전 / response를 되돌려 주기 전에 공통적으로 실행 할 친구들을 모아두었다.

말 그대로 "before_request" 와 "after_request" 이다.
- create_app : app을 선언하고, config파일을 불러오고 앱을 반환한다.
- get_flask_env : Config의 환경변수 파악 로직에 따라 production, develop으로 나뉘어 환경 설정을 받게 한다.

### manage.py

```python
from flask_script import Server, Manager
from app import create_app

app = create_app()
manager = Manager(app)
manager.add_command(
    "runserver",
    Server(host='0.0.0.0', port=5000, use_debugger=True)
)

if __name__ == "__main__":
    manager.run()
```

- [manage.py](http://manage.py)  는  flask-srcipt라는 친구를 알게되어서 사용 해 보게 되었다.
- flask-script는 차후에 더 정리 해 보려고 한다.
- 서버 실행과 실행 요소 설정들을 작업 해 준다. 이외의 설정 요소들은  app/__init__.py에서 모두 하고, [manage.py](http://manage.py) 는  완료된 app을 불러오기만 하면 된다.

### config/flask_config.py

```python
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

class Config(object):
    ENV = os.getenv('ENV')
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class devConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + os.environ["DB_USERNAME"] + ":" \
                              + os.environ["DB_PASSWORD"] + "@" \
                              + os.environ["DB_HOST"] + ":" \
                              + os.environ["DB_PORT"] + "/" \
                              + os.environ["DB_DATABASE"]

class prodConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + os.environ["DB_USERNAME"] + ":" \
                              + os.environ["DB_PASSWORD"] + "@" \
                              + os.environ["DB_HOST"] + ":" \
                              + os.environ["DB_PORT"] + "/" \
                              + os.environ["DB_DATABASE"]
```

- dotenv를 사용해서, .env파일을 추적하고 관련된 환경변수들을 받아온다.
- 지금은 기본 클래스인 Config과, Config을 상속받는 devConfig / prodConfig이 있다.
- 배포 서버가 나뉘는 것에 따라 여러가지를 추가 해도 될 것 같다.

### router/first_router (second_router도 비슷하다)

```python
from flask import jsonify, request, Blueprint

first = Blueprint('first_route', __name__)

@first.route("/first", methods=['GET'])
def first_route():
    msg = {
        "page": "first",
        "method": "GET"
    }
    return jsonify(msg)
```

- 사실 라우터는 Blueprint를 잘 사용하면 될 것 같다.
- Blueprint로 잘 나누어서 api의 endpoint를 잡아주면 될 것 같다.
- 내가 중요하게 생각 하는 요소 중 하나인데, router파일에는 정말 route와 로직을 실행 해 주는 provider 몇개를 만들어서 사용 해야 한다고 생각한다.
- 귀찮아서 그냥 router 내부에서 여러 함수들을 선언 할 수 있지만, 나중에 코드 정리하지뭐~ 하다가 치킨집을 먼저 차릴 수 도 있을...읍읍

### provider

- provider는 위의  router 에서 사용 될 '서비스'의 영역이다.
- 각 도메인 별로 나뉘기도 하고, 공통으로 사용 할 내용으로 나뉘기도 한다. 개발자 맘이지 뭐...
- api endpoint가 있는 router에 전달할 '정리된 데이터'를 만드는 역할을 한다고 생각하면 좋을 것 같다.

## 그래서 꼭 이대로 해야해?

절대 아니다. 프로젝트에 따라서 자유롭게 적용 하면 좋을 것 같다.

내가 이렇게 하면 좋겠다~ 해서 작성한 구조가 절대 정답이 아니다. 그냥 정리를 좋아한다.

좀더 컴팩트하게 정리하고 싶은 생각이든다.....!!!!!!

### 디비 커넥션

- 디비 커넥션은 Config에 넣었는데, 따로 빼는 분들도 있던 것 같다.
- 디비 모델을 불러오는 공간은 나는 model 로 두었다. 각 테이블 별로 파일을 만드는 것을 선호한다.

### 외부 pipeline

- 외부 파이프라인은 여러가지로 생각 할 것이 있는 것 같다.
- pipeline 환경설정 및 커넥션과 같은 것들은 Config에 몰아두거나 extConfig을 하나 더 선언하면 좋을 것 같다.
- pipeline을 사용해서 실제로 로직을 처리 하는 것은 provider안에 두어 작업 하는것이 좋을 것 같다.
- 괜히 rotuer쪽에 꼽아서 복잡하게 만들고 싶지 않다..