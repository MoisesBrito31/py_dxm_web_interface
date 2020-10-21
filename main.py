import subprocess
from threading import Thread

from server.server.Modbus import ModbusDados


def startServer():
    procss = subprocess.run(
        ['python', 'server/manage.py', 'runserver', '0.0.0.0:8000'],
        capture_output=False,
        text=True,
    )


server = Thread(target=ModbusDados, args=['192.168.0.100'])
server.run()
