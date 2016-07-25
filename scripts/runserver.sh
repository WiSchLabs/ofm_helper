#!/bin/bash

export DJANGO_SETTINGS_MODULE=ofm_helper.settings.prod

while getopts ":u:p:m:" opt; do
  case $opt in
    u)
	  USERNAME=$OPTARG
      ;;
    p)
	  PASSWORD=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

python3 manage.py migrate
echo "from users.models import OFMUser; OFMUser.objects.create_user(username='admin', password='admin', is_staff=True, is_superuser=True)" \
    | python manage.py shell
python3 manage.py runserver 0.0.0.0:8000