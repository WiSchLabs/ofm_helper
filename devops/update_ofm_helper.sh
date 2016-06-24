#!/bin/bash

set -o errexit -o nounset -o xtrace

cd repos/ofm_helper
git pull

/home/sh4ke/bin/pip3 install -r requirements.txt --user
# pip3 install -r prod_requirements.txt --user

export DJANGO_SETTINGS_MODULE=ofm_helper.settings.prod

python3 manage.py migrate
python3 manage.py collectstatic --no-input