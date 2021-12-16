.PHONY:  pip install lint importanize test run docker

pip:
	pip3 install -e src --extra-index-url=https://pypi.org/simple/

db:
	SHIPMNT_PROJECT_SETTINGS=configs/local.cfg \
	alembic upgrade head

db-upgrade:
	SHIPMNT_PROJECT_SETTINGS=configs/local.cfg \
	alembic upgrade head

db-alembic:
	SHIPMNT_PROJECT_SETTINGS=configs/local.cfg \
	alembic revision

install: pip

run:
	gunicorn --config=gunicorn.py shipmnt_project.wsgi

