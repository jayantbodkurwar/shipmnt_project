#! -*- coding: utf-8 -*-
import shutil
import subprocess
import sys

from . import app

# pylint: disable=invalid-name
application = app

# run alembic upgrade
print("running alembic upgrade")
executable = shutil.which("alembic")
command = [executable, "upgrade", "head"]
subprocess.run(command, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
print("alembic upgrade successful")
