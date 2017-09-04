# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse
from monitor.models import Reading, Meter
from pytz import timezone
import json#, datetime

ISO_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

def index(request):
    # yesterday = datetime.date.today() - datetime.day
    # readings = Reading.objects.filter(time__gte=yesterday)

    meter = Meter.objects.first()

    context = {'meter_id' : meter.id}

    return render(request, 'index.html', context)

def readings(request, meter_id):
    db_readings = get_list_or_404(Reading, meter__id=meter_id)[:1000]

    readings_dict = convert_readings_to_dict(db_readings)

    return JsonResponse(readings_dict)

def convert_readings_to_json(db_readings):
    return json.dumps(convert_readings_to_dict(db_readings))

def convert_readings_to_dict(db_readings):
    readings_list = []
    readings_dict = {'readings' : readings_list}

    local_tz = timezone('US/Central')

    for reading in db_readings:
        local_time = reading.time.astimezone(local_tz)
        readings_list.append({'time' : local_time.strftime(ISO_TIME_FORMAT), 
                              'consumption' : reading.consumption})

    return readings_dict