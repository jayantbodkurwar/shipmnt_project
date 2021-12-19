# -*- coding: utf-8 -*-
"""Setup module."""

from setuptools import find_packages, setup


setup(
    name="shipmnt-project",
    version="1.0.0",
    description="project for shipmnt",
    author="Jayant Bodkurwar",
    author_email="jayantreddybodkurwar",
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask==1.0.2",
        "gunicorn==19.9.0",
        "importanize==0.7.0",
        "python-gitlab==1.5.1",
        "flasgger==0.9.0",
        "flask_deprecate",
        "flask-migrate==2.2.1",
        "flask-sqlalchemy==2.3.2",
        "sqlalchemy-schemadisplay==1.3",
        "psycopg2-binary",
        "SQLAlchemy==1.3.22",
        "alembic==1.0.11",
        "pyjwt==1.7.1",
        "PyYAML==5.4.1"
    ],
)
