#!/bin/bash

export DJANGO_SETTINGS_MODULE=ofm_helper.settings.prod

python3 manage.py migrate

cat scripts/create_admin.py | python manage.py shell
python3 manage.py runserver 0.0.0.0:8000
