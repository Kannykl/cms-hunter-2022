#!/bin/bash


python manage.py makemigrations cms_hunter
python manage.py migrate
python manage.py collectstatic --no-input --clear
export DJANGO_SETTINGS_MODULE="config.settings"
python manage.py initadmin

python manage.py runserver 0.0.0.0:8000

exec "$@"
