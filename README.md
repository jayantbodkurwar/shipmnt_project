#   Shipment Project
"""
How to setup the Project ?
- Steps to run :
    1 - Create a virtual env with python 3.6 installed

    2 - Create a database in mysql with name shipment_project
    command - "create database shipmnt_project"

    3 - Clone the repository using 
    command - "git clone https://github.com/jayantbodkurwar/shipmnt_project.git"

    4 - Run Make install command to install all dependencies
    command - "cd shipmnt_project"
              "make install"
    // Prerequisite - Please have Pip version set to 21.1.2"

    5 - Run Make db command to run alembic and setup tables inside database
    command -  "make db"

    6 - Run Make run command to launch the flask application
    command -  "make run"

    7 - Open the below mentioned link to access the service.
    link - "http://0.0.0.0:9000/vcs/api/docs"


