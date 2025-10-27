#!/bin/sh
# entrypoint.sh
python /usr/src/app/manage.py migrate
python /usr/src/app/manage.py createsuperuser --noinput
exec "$@"