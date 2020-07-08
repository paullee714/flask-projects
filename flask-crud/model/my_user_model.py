# coding: utf-8
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class MyUser(db.Model):
    """
        table name : my_user
        table info
            - id : index id
            - user name
            - created_at
            - updated_at
    """
    __tablename__ = 'my_user'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_name = db.Column(db.String(20, 'utf8mb4_unicode_ci'))
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    udpated_at = db.Column(db.DateTime, server_default=db.FetchedValue())

    def __init__(self, user_name, created_at, updated_at):
        self.user_name = user_name
        self.created_at = created_at
        self.udpated_at = updated_at
