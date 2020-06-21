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
