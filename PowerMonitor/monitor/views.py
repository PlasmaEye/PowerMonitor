# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from models import Reading
from pytz import timezone
import datetime, pytz, json

TIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

def index(request):
    # yesterday = datetime.date.today() - datetime.day
    # readings = Reading.objects.filter(time__gte=yesterday)

    db_readings = Reading.objects.order_by('time')[:1440]

    readings = []

    local_tz = timezone('US/Central')

    for reading in db_readings:
        local_time = reading.time.astimezone(local_tz)
        readings.append({'time' : local_time.strftime(TIME_FORMAT), 'consumption' : reading.consumption})    

    context = { 'reading_list' : json.dumps(readings) }

    return render(request, 'index.html', context)