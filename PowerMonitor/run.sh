#!/bin/bash
redis-server &
celery -A PowerMonitor worker -l info -B --scheduler django_celery_beat.schedulers:DatabaseScheduler &
python manage.py runserver 0:8000