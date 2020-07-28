# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.ext.declarative import declarative_base
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(20), primary_key=True, nullable=False)
    useremail = Column(String(100))
    userpwd = Column(String(100), nullable=False)
    bio = Column(Text)
    created_at = Column(DateTime, server_default=FetchedValue())
    updated_at = Column(DateTime, server_default=FetchedValue())

    def has_password(self):
        self.userpwd = generate_password_hash(self.userpwd).decode('utf8')

    def check_password(self,password):
        return check_password_hash(self.userpwd,password)
