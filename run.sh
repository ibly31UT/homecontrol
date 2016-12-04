#!/bin/sh
if [ "$#" -eq 0 ]; then
    python manage.py runserver 0.0.0.0:8000
fi
if [ "$#" -eq 1 ]; then
    if [ "$1" = "reset" ]; then
        rm db.sqlite3
        rm -rf hc/migrations
        python manage.py makemigrations hc
        python manage.py migrate
        python manage.py loaddata initdata.json
    fi
fi