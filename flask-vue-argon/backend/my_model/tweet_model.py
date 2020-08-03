# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Tweet(db.Model):
    __tablename__ = 'tweet'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    words = db.Column(db.Text, nullable=False)
    creator = db.Column(db.String(100), nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.FetchedValue())
    updated_at = db.Column(db.DateTime, server_default=db.FetchedValue())

    def to_dict(self):
        return dict(id=self.id,
                    title=self.title,
                    words=self.words,
                    creator=self.creator,
                    created_at=self.created_at,
                    updated_at=self.updated_at)
