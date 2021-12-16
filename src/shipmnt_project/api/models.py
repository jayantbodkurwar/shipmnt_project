import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import g

db = SQLAlchemy()


class Version(db.Model):
    __tablename__ = "question_details"
    id = db.Column(db.Integer, primary_key=True, )
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
    answer_id = db.Column(db.Integer, primary_key=True, )
    user_id = db.Column(db.String(255), unique=False, nullable=False)
    user_name = db.Column(db.String(255), unique=False, nullable=False)
    question_body = db.Column(db.String(1000), unique=False, nullable=False)
    answer = db.Column(db.JSON, unique=False, nullable=False)
    upvote = db.Column(db.Integer, unique=False, nullable=True)
    downvote = db.Column(db.Integer, unique=False, nullable=True)


    def as_dict(self):
        """ Dict representation """
        return {c.name: str(getattr(self, c.name)) if isinstance(getattr(self, c.name), datetime.datetime) else getattr(self, c.name) for c in self.__table__.columns}


