# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import JsonResponse
from monitor.models import Reading
from pytz import timezone
import json#, datetime

ISO_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

def index(request):
    # yesterday = datetime.date.today() - datetime.day
    # readings = Reading.objects.filter(time__gte=yesterday)

    db_readings = Reading.objects.order_by('time')[:1440]

    json_Readings = convert_readings_to_json(db_readings)

    context = {'reading_list' : json.dumps(json_Readings)}

    return render(request, 'index.html', context)

def readings(request, meter_id):
    db_readings = Reading.objects.filter(meter__id=meter_id).in_bulk()

    readings_dict = convert_readings_to_dict(db_readings)

    return JsonResponse(readings_dict)

def convert_readings_to_json(db_readings):
    return json.dumps(convert_readings_to_dict(db_readings))

def convert_readings_to_dict(db_readings):
    readings_dict = []

    local_tz = timezone('US/Central')

    for reading in db_readings:
        local_time = reading.time.astimezone(local_tz)
        readings_dict.append({'time' : local_time.strftime(ISO_TIME_FORMAT), 'consumption' : reading.consumption})

    return readings_dict