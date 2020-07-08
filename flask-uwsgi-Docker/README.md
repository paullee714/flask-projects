# Flask with Docker, uwsgi

wsgi를 사용한 Flask

> wsgi는 CGI(Common Gateway Interface)의 일종으로, web이 이제 막 걸음마 단계를 시작했을 적에 CGI는 수많은 언어에서 문제 없이 작동한다는 이유로(애초에 CGI 외에 다른 선택권이 없기도 했다) 기하급수적으로 사용량이 증가했다. 하지만 CGI는 너무 느리고 제한사항도 많았을 뿐더러, python app에서는 CGI, mod_python, Fast CGI 등등 만을 사용했다. wsgi는 이와중에 프레임워크의 웹서버로, route web에서는 표준 인터페이스로 개발되었다.
출처: [https://paphopu.tistory.com/entry/WSGI에-대한-설명-WSGI란-무엇인가](https://paphopu.tistory.com/entry/WSGI%EC%97%90-%EB%8C%80%ED%95%9C-%EC%84%A4%EB%AA%85-WSGI%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80) [jadehan]

wsgi 서버는 많은 request들을 다룰 수 있도록 설계되었다. Django나 Flask의 개발 용 내장서버 (manage.py , flask run)는 테스트를 간단하게 할 수 는 있지만 다량의 Request들을 다루기에 적합하지 않다.

여러 wsgi들 중에 uwsgi를 사용하여 Flask, Docker에 적용 해 볼 계획이다.

# Flask with Docker, uwsgi

## Flask 시작

여러번 다루었지만, Flask 서버를 시작하기 위해서 가상환경과 필요 패키지들을 설치 해 주도로 하겠다.

### Project structure

```
.
├── Dockerfile
├── app.py
└── uwsgi.ini
```

### Flask, uwsgi 설치

```bash
$ virtualenv venv
$ source venv/bin/activate
(venv)$ pip install flask uwsgi
```

### app.py

```python
from flask import Flask

app = Flask(__name__)

@app.route('/',methods=['GET'])
def index():
	return "hi!"

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5050)
```

### Dockerfile

```docker
FROM python:3

ADD . /www
WORKDIR /www

RUN python3 -m pip install -U pip
RUN pip3 install flask
RUN pip3 install uwsgi

CMD uwsgi uwsgi.ini
```

### uwsgi.ini

```
[uwsgi]
chdir=/www/
http-socket=:5050
wsgi-file=/www/app.py
callable=app
master=true
processes=4
threads=2
vacuum = true
disable-logging=True
```

ini 파일에서 실행에 추가적인 옵션들을 더 줄 수 있다.

Nginx까지 사용하는 서버라면, http-socket대신 socket를 쓸 수 도 있다.

특히 disable-logging=True 옵션은, Flask 내에서 생성되는 로그와 uwsgi의 로그가 중첩되는 것을 막아준다

## Docker Images 빌드 및 실행

```bash
$ Docker build -t flask_wool

$ docker run -it -p 5050:5050 flask_wool
```

## 테스트 해 보기

두가지로 테스트 할 수 있다.

1. 사파리, 크롬 등을 사용해서  [localhost:5050](http://localhost:5050) 에 접속 해서 확인
2. 커맨드로 확인하기

    ```bash
    $ curl -X GET http://localhost:5050

    hi!
    ```