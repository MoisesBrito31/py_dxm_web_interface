import subprocess
from threading import Thread


def startServer():
    procss = subprocess.run(
        ['python', 'server/manage.py', 'runserver', '0.0.0.0:8000'],
        capture_output=False,
        text=True
    )


server = Thread(target=startServer, args={})
server.run()
