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
