# Power Monitor

Use the [rtlamr library](https://github.com/bemasher/rtlamr) to read power meter readings periodically. Uses [Celery](http://www.celeryproject.org/) and [Redis](https://redis.io/) to schedule tasks to read the power meters. [Django](https://www.djangoproject.com/) is used to store, retrieve, and display readings.

## Installation

Build and run [rtltcp](github.com/bemasher/rtltcp) on a device that has an rtl-sdr USB dongle. Build a version of the rtlamr library and place it in the lib folder. Modify the rtltcpAddress in monitor/tasks.py to the rtltcp server address.

## Operation

Run the run.sh shell script to start the Redis server, Celery worker, and Django server.

```bash
./run.sh
```

Ctrl-C to stop everything.