# Power Monitor

Use the [rtlamr library](https://github.com/bemasher/rtlamr) to read power meter readings periodically. Uses [Celery](http://www.celeryproject.org/) and [Redis](https://redis.io/) to schedule tasks to read the power meters. [Django](https://www.djangoproject.com/) is used to store, retrieve, and display readings.

## Installation

Build and run [rtltcp](github.com/bemasher/rtltcp) on a device that has an rtl-sdr USB dongle. Build a version of the rtlamr library and place it in the lib folder. Modify the rtltcpAddress in monitor/tasks.py to the rtltcp server address.

## Operation

Run redis.

```bash
redis-server
```

Run celery with the following command:

```bash
celery -A PowerMonitor worker -l info -B --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

Run the Django server:

```bash
python manage.py runserver
```

In the admin panel, add a task to run recordReading every 5 minutes.