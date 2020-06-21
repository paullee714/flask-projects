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

app.secret_key = 'qwerqwer123'

if __name__ == '__main__':
    
    app.run(debug=True)