#!/bin/bash

export DJANGO_SETTINGS_MODULE=ofm_helper.settings.prod

python3 manage.py migrate
echo "from users.models import OFMUser; if not OFMUser.objects.get(username='admin'): OFMUser.objects.create_user(username='admin', password='admin', is_staff=True, is_superuser=True)" \
    | python manage.py shell
python3 manage.py runserver 0.0.0.0:8000
