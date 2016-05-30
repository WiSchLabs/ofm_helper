#!/bin/bash
rm -vrf core/migrations/* player_statistics/migrations/* db.sqlite3
./manage.py core player_statistics
./manage.py migrate
