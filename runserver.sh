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
    m)
	  EMAIL=$OPTARG
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

echo "from django.contrib.auth.models import User; User.objects.create_superuser('$USERNAME', '$EMAIL', '$PASSWORD')" \
    | python manage.py shell
python3 manage.py runserver 0.0.0.0:8000
