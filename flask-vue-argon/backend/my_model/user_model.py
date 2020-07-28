# coding: utf-8
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), primary_key=True, nullable=False)
    useremail = db.Column(db.String(100))
    userpwd = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, server_default=db.FetchedValue())


    def has_password(self):
        self.userpwd = generate_password_hash(self.userpwd).decode('utf8')

    def check_password(self,password):
        return check_password_hash(self.userpwd,password)
