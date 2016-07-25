#!/bin/bash

set -o errexit -o nounset -o xtrace

cd repos/ofm_helper

export DJANGO_SETTINGS_MODULE=ofm_helper.settings.prod

python3 manage.py runcrons