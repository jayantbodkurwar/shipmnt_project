import json
import logging

from flask_sqlalchemy import SQLAlchemy

from .models import db as version_db
from .models import Version as Version
from .models import Answers as Answers


class DatabaseApi:
    LOG = logging.getLogger("vcs.database_api.log")

    db_obj = None
    app = None

    def __init__(self, app):
        version_db.init_app(app)
        self.db_obj = SQLAlchemy(app)
        self.app = app

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
            version = Version(
                user_id=user_id,
                user_name=user_name,
                question_title=question_title,
                question_body=question_body,
                tags=question_tags)
            self.db_obj.session.add(version)
            self.db_obj.session.flush()
            self.db_obj.session.commit()
            return version
        except Exception as ex:
            self.LOG.exception(ex)
            raise ValueError("Failed saving entry in database")

    def post_answer(self, user_id, user_name, question_body, answer):

        try:
            answer = Answers(
                user_id=user_id,
                user_name=user_name,
                question_body=question_body,
                answer=answer)
            self.db_obj.session.add(answer)
            self.db_obj.session.flush()
            self.db_obj.session.commit()
            return answer
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

    def vote(self, parameter, answer_id):
        versions = []

        try:
            if parameter == 'upvote':
                vote = self.db_obj.session.query(Answers.upvote) \
                    .filter_by(answer_id=answer_id) \
                    .all()
            elif parameter == 'downvote':
                vote = self.db_obj.session.query(Answers.downvote) \
                    .filter_by(answer_id=answer_id) \
                    .all()                
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
                DatabaseApi.create_new_questios_recor(self,user_id=res['user_id'], user_name=res['user_name'], question_title=res['question_title'], question_body=res['question_body'], question_tags=res['tags'])
                self.db_obj.session.query(Version).filter_by(id=question_id).delete()
                self.db_obj.session.commit()
                return("Successfully Updated the question")
            else:
                return("You dont have the access to update this entry")
        except Exception as ex:
            self.LOG.exception(ex)
            return json.dumps(versions)

