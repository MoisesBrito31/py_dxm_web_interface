#! /bin/bash

ifconfig enp0s8 169.254.48.24 netmask 255.255.0.0 up

cd /home/moises/py_dxm_web_interface/server

.venv/bin/python manage.py runserver 0.0.0.0:8000
