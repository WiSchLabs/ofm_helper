#!/bin/bash

export DJANGO_SETTINGS_MODULE=ofm_helper.settings.prod

python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
