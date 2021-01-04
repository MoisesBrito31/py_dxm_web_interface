import subprocess
from datetime import datetime
from time import sleep


def startServer():
    procss = subprocess.run(
        ['python', 'server/manage.py', 'runserver', '0.0.0.0:8000'],
        capture_output=False,
        text=True,
    )


startServer()


