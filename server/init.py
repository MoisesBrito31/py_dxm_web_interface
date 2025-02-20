import os
from time import sleep
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

def run_server():
    execute_from_command_line(["manage.py", "runserver","0.0.0.0:8000","--noreload"])

if __name__ == "__main__":
    os.system("start http://localhost:8000")
    run_server()
    