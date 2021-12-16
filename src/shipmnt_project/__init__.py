# -*- coding: utf-8 -*-

"""Init module."""

import os

from uuid import uuid4

import json

from urllib.parse import urlparse
from flasgger import Swagger

from flask import Flask, Response, jsonify, request, g, Blueprint, current_app
from flasgger import swag_from

from .api.database_api import DatabaseApi as DatabaseApi
from .api.models import Version as Version

app = Flask(__name__)

# initialize settings
base_path = os.path.dirname(os.path.realpath(__file__))
default = os.path.join(base_path, "configs", "local.cfg")
config_file = os.getenv("SHIPMNT_PROJECT", default)
app.config.from_pyfile(config_file)



shipmnt_project = Blueprint("shipmnt_project", __name__)
# register blue prints
url_prefix = app.config["URL_PREFIX"]

# define swagger
swagger_template = {
    "swagger": "1.0",
    "info": {
        "title": "Shipment Project",
        "description": "REST API's for interacting with Project",
        "contact": {
            "responsibleOrganization": "Shipment",
            "responsibleDeveloper": "Jayant Bodkurwar",
        },
        "version": "1.0.0",
    },
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "specifications",
            "route": "{}/docs/specifications.json".format(app.config["URL_PREFIX"]),
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "{}/flasgger_static".format(app.config["URL_PREFIX"]),
    "swagger_ui": True,
    "specs_route": "{}/docs".format(app.config["URL_PREFIX"]),
}

Swagger(app, config=swagger_config, template=swagger_template)

app_config = app.config

DB_API = DatabaseApi(app=app)

@shipmnt_project.before_request
def authentication():
    """ Authentication middleware """

    # skip auth
    if skip_authentication():
        return


# Every request will filter here before hit actual rest end point URL
@shipmnt_project.before_request
def before_request():
    """ Middleware to inject request and validate attribute in request headers"""
    # parse headers to get request id and project id
    request_id = request.headers.get('Request-Id', str(uuid4()))


def skip_authentication():
    skip_auth = app.config["SKIP_AUTH"]
    url = request.url
    if [auth_url for auth_url in skip_auth if auth_url in url]:
        return True


@shipmnt_project.route("/v1/ping")
@swag_from("swags/ping.yaml")
def pong():
    """ Endpoint used to check the health of the service """
    return Response("pong")

@shipmnt_project.route("/v2/question", methods=["POST"])
@swag_from("swags/post_question.yaml")
def post_questions():
    """
    API to post new questions
    """
    try:
        user_id = request.headers.get("X-Auth-Userid")
        user_name = request.headers.get("X-Auth-Username")
        question_title = request.headers.get("Title")
        question_body = request.headers.get("Question")
        question_tags = request.headers.get("tags")

        question_id = DB_API.create_new_questios_recor(
            user_id=user_id,
            user_name=user_name,
            question_title=question_title,
            question_body=question_body,
            question_tags=question_tags)
        return Response("Successfully posted the Question", status=201)
    except Exception as ex:
        current_app.logger.exception(ex)
        return Response(ex.args[0], status=500)

@shipmnt_project.route("/v2/answer", methods=["POST"])
@swag_from("swags/post_answer.yaml")
def post_answers():
    """
    API to post answers
    """

    try:
        user_id = request.headers.get("X-Auth-Userid")
        user_name = request.headers.get("X-Auth-Username")
        question_body = request.headers.get("Question")
        answer = request.get_json()

        question_id = DB_API.post_answer(
            user_id=user_id,
            user_name=user_name,
            question_body=question_body,
            answer=answer)
        return Response("Successfully posted an Answer", status=201)
    except Exception as ex:
        current_app.logger.exception(ex)
        return Response(ex.args[0], status=500)

@shipmnt_project.route("/v2/vote_answer", methods=["POST"])
@swag_from("swags/upvote_answer.yaml")
def upvote_answers():
    """
    API to upvote answers
    """
    try:
        answer_id = request.headers.get("Answer_id")
        parameter = request.headers.get("Parameter")

        id = DB_API.vote(parameter, answer_id)
        return Response("Successfully upvoted an Answer", status=201)
    except Exception as ex:
        current_app.logger.exception(ex)
        return Response(ex.args[0], status=500)


@shipmnt_project.route("/v2/question", methods=["GET"])
@swag_from("swags/get_question.yaml")
def get_questions():
    """
    #API to get all questions
    """
    try:
        parameter = request.headers.get("Parameter")
        value = request.headers.get("Value")

        if parameter == "user_id":
            return Response(DB_API.fetch_questions_by_userid(value),status=200,mimetype="application/json")
        if parameter == "user_name":
            return Response(DB_API.fetch_questions_by_username(value),status=200,mimetype="application/json")
        if parameter == "question_title":
            return Response(DB_API.fetch_questions_by_title(value),status=200,mimetype="application/json")
        if parameter == "tags":
            return Response(DB_API.fetch_questions_by_tags(value),status=200,mimetype="application/json")
    except Exception as ex:
        current_app.logger.exception(ex)
        return Response(ex.args[0], status=500)


@shipmnt_project.route("/v2/all_question", methods=["GET"])
@swag_from("swags/get_all_question.yaml")
def get_all_questions():
    """
    #API to get all questions
    """
    try:
        return Response(DB_API.fetch_all_questions(),status=200,mimetype="application/json")
    except Exception as ex:
        current_app.logger.exception(ex)
        return Response(ex.args[0], status=500)

@shipmnt_project.route("/v2/all_answers", methods=["GET"])
@swag_from("swags/get_all_answers.yaml")
def get_all_answer():
    """
    #API to get all answers
    """
    try:
        return Response(DB_API.fetch_question_answer(),status=200,mimetype="application/json")
    except Exception as ex:
        current_app.logger.exception(ex)
        return Response(ex.args[0], status=500)

@shipmnt_project.route("/v2/question", methods=["PUT"])
@swag_from("swags/update_question.yaml")
def update_questions():
    """
    #API to update questions
    """
    try:
        user_id = request.headers.get("X-Auth-Userid")
        question_id = request.headers.get("Question_id") 
        parameter = request.headers.get("Parameter")
        value = request.headers.get("Value")
        return(DB_API.update_question(user_id, question_id, parameter, value))
    except Exception as ex:
        current_app.logger.exception(ex)
        return Response(ex.args[0], status=500)

app.register_blueprint(shipmnt_project, url_prefix=url_prefix)