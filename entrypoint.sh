#!/bin/sh
set -x   # show commands
set -e

python manage.py migrate --noinput || echo "MIGRATE FAILED"
python manage.py collectstatic --noinput || echo "STATIC FAILED"

gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000
