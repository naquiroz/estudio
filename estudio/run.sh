#!/bin/bash

if [ "$DJANGO_ENV" = "DEVELOPMENT" ]; then
    exec gunicorn --bind 0.0.0.0:$PORT estudio.wsgi --reload --log-level debug
else
    exec gunicorn --bind 0.0.0.0:$PORT estudio.wsgi --threads=2 --workers=3 --timeout 60 --log-level info
fi
