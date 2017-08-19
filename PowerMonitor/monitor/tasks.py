from celery import shared_task
from models import Meter, Reading
from subprocess import call

@shared_task
def recordReading():
    print "recordReading"