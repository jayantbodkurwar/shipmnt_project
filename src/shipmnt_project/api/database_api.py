import json
import logging
from flask_sqlalchemy import SQLAlchemy

from .models import db as version_db
from .models import Version as Version
from .models import Answers as Answers
from .models import Users as Users
from .models import Voting as Voting
import ast
import jwt
from uuid import uuid4
from werkzeug.security import check_password_hash
import datetime
from flask import jsonify


class DatabaseApi:
    LOG = logging.getLogger("vcs.database_api.log")

    db_obj = None
    app = None

    def __init__(self, app):
        version_db.init_app(app)
        self.db_obj = SQLAlchemy(app)
        self.app = app


    def register_user(self, user_name, hashed_password):

        try:
            user = self.db_obj.session.query(Users).filter_by(user_name=user_name).first()
            if user:
                return("User already exist")
            new_user = Users(public_id=str(uuid4()), user_name=user_name, password=hashed_password)
            self.db_obj.session.add(new_user) 
            self.db_obj.session.commit()
            return("Successfully registered a user")
        except Exception as ex:
            self.LOG.exception(ex)
            raise ValueError("Failed saving entry in database")

    def validate_user(self, user_name, password):
        try:
            user = self.db_obj.session.query(Users).filter_by(user_name=user_name).first()

            if check_password_hash(user.password, password):
                token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=45)}, 'GkeE6mK7CBt4EUS03Zl0HgMcnEQ/RL+MnqksukdjbS2JJxXY3wgvl+Naldk5yLJ/SHyWmHugQ', "HS256")
            
            return('token for the logged in user: ' +token.decode("utf-8"))
        except Exception as ex:
            self.LOG.exception(ex)
            raise ValueError("Could not verify, Authentication failed")

    def create_new_questios_recor(self,
                                  user_id,
                                  user_name,
                                  question_title,
                                  question_body,
                                  question_tags):
        """
        :param used_id: used_id
        :param user_name: user_name
        :param question_title: question_title
        :param question_body: question_body
        :param question_tags: question_tags
        :return: question_id
        """
        
        
        try:
            #check if question is already posted
            result = DatabaseApi.check_if_question_exist(self, question_body)
            res = json.loads(result)
            if res:
                return("Question already exist, posted by ",res[0]['user_id'] ," with question_id ", res[0]['id'])
            version = Version(
                user_id=user_id,
                user_name=user_name,
                question_title=question_title,
                question_body=question_body,
                tags=question_tags)
            self.db_obj.session.add(version)
            self.db_obj.session.flush()
            self.db_obj.session.commit()
            return("Successfully posted a question")
        except Exception as ex:
            self.LOG.exception(ex)
            raise ValueError("Failed saving entry in database")

    def check_if_question_exist(self, value):
        versions = []
        try:
            versions = self.db_obj.session.query(Version) \
                .filter_by(question_body=value) \
                .all()
            return json.dumps([version.as_dict() for version in versions])
        except Exception as ex:
            self.LOG.exception(ex)
            return json.dumps(versions)        

    def post_answer(self, user_id, user_name, question_id, answer):
        try:
            result = DatabaseApi.fetch_questions_by_questionid(self, question_id)
            res = ast.literal_eval(result)
            if res:  
                answer = Answers(
                    question_id=question_id,
                    user_id=user_id,
                    user_name=user_name,
                    question_body=res[0]['question_body'],
                    answer=answer)
                self.db_obj.session.add(answer)
                self.db_obj.session.flush()
                self.db_obj.session.commit()
                return("Successfully posted an Answer")
            else:
               return("Incorrect Question_Id, No such question exists") 
        except Exception as ex:
            self.LOG.exception(ex)
            raise ValueError("Failed saving entry in database")

    def fetch_question_answer(self):
        versions = []
        try:
            versions = self.db_obj.session.query(Answers) \
                .all()
            return json.dumps([version.as_dict() for version in versions])
        except Exception as ex:
            self.LOG.exception(ex)
            return json.dumps(versions)      

    def vote(self, user_id, parameter, answer_id):
        versions = []

        try:
            upside = self.db_obj.session.query(Voting.upvote).filter_by(user_id=user_id).filter_by(answer_id=answer_id).all()
            downside = self.db_obj.session.query(Voting.downvote).filter_by(user_id=user_id).filter_by(answer_id=answer_id).all()
            if parameter == 'upvote':
                vote = self.db_obj.session.query(Answers.upvote) \
                    .filter_by(answer_id=answer_id) \
                    .all()
                if len(upside)==0:
                    upside = 1
                    voting = Voting(answer_id=answer_id,user_id=user_id,upvote=upside,downvote=len(downside))
                    self.db_obj.session.add(voting)
                    self.db_obj.session.flush()
                    self.db_obj.session.commit()
                    return("Successfully upvote the answer")
                elif upside[0][0]==0:
                    upside = 1
                    voting = self.db_obj.session.query(Voting).filter_by(user_id=user_id).filter_by(answer_id=answer_id).update(dict(upvote=upside))
                    self.db_obj.session.commit()
                    return("Successfully upvote the answer")
                elif upside[0][0]==1:
                    return("Already upvoted the answer. Cannot do it twice")
            elif parameter == 'downvote':
                vote = self.db_obj.session.query(Answers.downvote) \
                    .filter_by(answer_id=answer_id) \
                    .all()   
                if len(downside)==0:
                    downside = 1
                    voting = Voting(answer_id=answer_id,user_id=user_id,upvote=len(upside),downvote=downside)
                    self.db_obj.session.add(voting)
                    self.db_obj.session.flush()
                    self.db_obj.session.commit()  
                    return("Successfully downvoted the answer")            
                elif downside[0][0]==0:
                    downside = 1
                    voting = self.db_obj.session.query(Voting).filter_by(user_id=user_id).filter_by(answer_id=answer_id).update(dict(downvote=downside))
                    self.db_obj.session.commit()
                    return("Successfully downvoted the answer")
                elif downside[0][0]==1:
                    return("Already downvoted the answer. Cannot do it twice")

            value = vote[0][0]
            if value is None:
                value = 1
            else:
                value = int(value) + 1
            if parameter == 'upvote':
                version=self.db_obj.session.query(Answers).filter_by(answer_id=answer_id).update(dict(upvote=value))
            elif  parameter == 'downvote':
                version=self.db_obj.session.query(Answers).filter_by(answer_id=answer_id).update(dict(downvote=value))
            self.db_obj.session.commit()
            return json.dumps([version.as_dict() for version in versions])
        except Exception as ex:
            self.LOG.exception(ex)
            return json.dumps(versions)

    def fetch_questions_by_userid(self, value):
        versions = []
        try:
            versions = self.db_obj.session.query(Version) \
                .filter_by(user_id=value) \
                .all()
            return json.dumps([version.as_dict() for version in versions])
        except Exception as ex:
            self.LOG.exception(ex)
            return json.dumps(versions)

    def fetch_questions_by_questionid(self, value):
        versions = []
        try:
            versions = self.db_obj.session.query(Version) \
                .filter_by(id=value) \
                .all()
            return json.dumps([version.as_dict() for version in versions])
        except Exception as ex:
            self.LOG.exception(ex)
            return json.dumps(versions)

    def fetch_questions_by_username(self, value):
        versions = []
        try:
            versions = self.db_obj.session.query(Version) \
                .filter_by(user_name=value) \
                .all()
            return json.dumps([version.as_dict() for version in versions])
        except Exception as ex:
            self.LOG.exception(ex)
            return json.dumps(versions)

    def fetch_questions_by_title(self, value):
        versions = []
        try:
            versions = self.db_obj.session.query(Version) \
                .filter_by(question_title=value) \
                .all()
            return json.dumps([version.as_dict() for version in versions])
        except Exception as ex:
            self.LOG.exception(ex)
            return json.dumps(versions)


    def fetch_questions_by_tags(self, value):
        versions = []
        try:
            tag = value
            search = "%{}%".format(tag)
            versions = self.db_obj.session.query(Version) \
                .filter(Version.tags.like(search)) \
                .all()
            return json.dumps([version.as_dict() for version in versions])
        except Exception as ex:
            self.LOG.exception(ex)
            return json.dumps(versions)

    def fetch_all_questions(self):
        versions = []
        try:
            versions = self.db_obj.session.query(Version) \
                .all()
            return json.dumps([version.as_dict() for version in versions])
        except Exception as ex:
            self.LOG.exception(ex)
            return json.dumps(versions)

    def update_question(self, user_id, question_id, parameter, value):
        try:
            versions = self.db_obj.session.query(Version) \
                .filter_by(id=question_id) \
                .all()
            
            delete=json.dumps([version.as_dict() for version in versions])
            deleted = delete[1:-1]
            res = json.loads(deleted)
            if res['user_id'] == user_id:
                res[parameter] = value
                self.db_obj.session.query(Version).filter_by(id=question_id).delete()
                self.db_obj.session.commit()
                DatabaseApi.create_new_questios_recor(self,user_id=res['user_id'], user_name=res['user_name'], question_title=res['question_title'], question_body=res['question_body'], question_tags=res['tags'])
                return("Successfully Updated the question")
            else:
                return("You dont have the access to update this entry")
        except Exception as ex:
            self.LOG.exception(ex)
            return json.dumps(versions)

