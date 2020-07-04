from flask import Flask
from route.app_route import app_route

app = Flask(__name__)

app.register_blueprint(app_route)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
