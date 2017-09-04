# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json#, datetime
from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse
from monitor.models import Reading, Meter
from pytz import timezone
from datetime import timedelta

ISO_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

def index(request):
    # yesterday = datetime.date.today() - datetime.day
    # readings = Reading.objects.filter(time__gte=yesterday)

    meter = Meter.objects.first()

    context = {'meter_id' : meter.id}

    return render(request, 'index.html', context)

def readings(request, meter_id):
    db_readings = get_list_or_404(Reading, meter__id=meter_id)[:20]

    to_convert = []
    time_anchor = db_readings[0].time
    consumption_anchor = db_readings[0].consumption

    for reading in db_readings:
        time_span = reading.time - time_anchor
        if time_span > timedelta(minutes=5):
            to_convert.append({'time': time_anchor + timedelta(minutes=5), 'consumption': 0})
            to_convert.append({'time': reading.time - timedelta(minutes=5), 'consumption': 0})

        to_convert.append({'time': reading.time, 'consumption': reading.consumption - consumption_anchor})            
        consumption_anchor = reading.consumption
        time_anchor = reading.time

    readings_dict = convert_readings_to_dict(to_convert)

    return JsonResponse(readings_dict)

def convert_readings_to_dict(db_readings):
    readings_list = []
    readings_dict = {'readings' : readings_list}

    local_tz = timezone('US/Central')

    for reading in db_readings:
        local_time = reading['time'].astimezone(local_tz)
        readings_list.append({'time' : local_time.strftime(ISO_TIME_FORMAT), 
                              'consumption' : reading['consumption']})

    return readings_dict