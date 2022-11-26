#!/bin/sh

python manage.py collectstatic --no-input && python manage.py migrate && daphne mysite.asgi:application -b 0.0.0.0 -p 80