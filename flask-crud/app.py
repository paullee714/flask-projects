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
