import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import g
from uuid import uuid4
import jwt
from functools import wraps
from flask import Flask, Response, jsonify, request, g, Blueprint, current_app

db = SQLAlchemy()


class Version(db.Model):
    __tablename__ = "question_details"
    id = db.Column(db.String(60), primary_key=True, default=str(uuid4()))
    user_id = db.Column(db.String(255), unique=False, nullable=False)
    user_name = db.Column(db.String(255), unique=False, nullable=False)
    question_title = db.Column(db.String(1000), unique=False, nullable=False)
    question_body = db.Column(db.String(1000), unique=False, nullable=False)
    tags = db.Column(db.String(1000), unique=False, nullable=True)

    def as_dict(self):
        """ Dict representation """
        return {c.name: str(getattr(self, c.name)) if isinstance(getattr(self, c.name), datetime.datetime) else getattr(self, c.name) for c in self.__table__.columns}

class Answers(db.Model):
    __tablename__ = "question_answers"
    answer_id = db.Column(db.String(60), primary_key=True, default=str(uuid4()))
    question_id = db.Column(db.String(255), unique=False, nullable=False)
    user_id = db.Column(db.String(255), unique=False, nullable=False)
    user_name = db.Column(db.String(255), unique=False, nullable=False)
    question_body = db.Column(db.String(1000), unique=False, nullable=False)
    answer = db.Column(db.String(1000), unique=False, nullable=False)
    upvote = db.Column(db.Integer, unique=False, nullable=True)
    downvote = db.Column(db.Integer, unique=False, nullable=True)


    def as_dict(self):
        """ Dict representation """
        return {c.name: str(getattr(self, c.name)) if isinstance(getattr(self, c.name), datetime.datetime) else getattr(self, c.name) for c in self.__table__.columns}

class Voting(db.Model):
    __tablename__ = "vote_answers"
    id = db.Column(db.String(60), primary_key=True, default=str(uuid4()))
    answer_id = db.Column(db.String(60), unique=False, nullable=False)
    user_id = db.Column(db.String(255), unique=False, nullable=False)
    upvote = db.Column(db.Integer, unique=False, nullable=True)
    downvote = db.Column(db.Integer, unique=False, nullable=True)

    def as_dict(self):
        """ Dict representation """
        return {c.name: str(getattr(self, c.name)) if isinstance(getattr(self, c.name), datetime.datetime) else getattr(self, c.name) for c in self.__table__.columns}


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(60), primary_key=True, default=str(uuid4()))
    public_id = db.Column(db.String(60))
    user_name = db.Column(db.String(255), unique=False, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)

    def as_dict(self):
        """ Dict representation """
        return {c.name: str(getattr(self, c.name)) if isinstance(getattr(self, c.name), datetime.datetime) else getattr(self, c.name) for c in self.__table__.columns}


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'X-ACCESS-TOKEN' in request.headers:
            token = request.headers['X-ACCESS-TOKEN']
            print(token)
        
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, 'GkeE6mK7CBt4EUS03Zl0HgMcnEQ/RL+MnqksukdjbS2JJxXY3wgvl+Naldk5yLJ/SHyWmHugQ', algorithms=["HS256"])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        
        return f(current_user, *args, **kwargs)
    return decorator
    