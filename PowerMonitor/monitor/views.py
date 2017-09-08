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
    db_readings = get_list_or_404(Reading, meter__id=meter_id)[19:]

    to_convert = []
    time_anchor = db_readings[0].time
    consumption_anchor = db_readings[0].consumption

    iter_readings = iter(db_readings)
    next(iter_readings)

    for reading in iter_readings:
        time_span = reading.time - time_anchor
        consumption = reading.consumption - consumption_anchor

        seconds_in_hour = 60 * 60        
        hours_elapsed = time_span.total_seconds() / seconds_in_hour
        kw_per_hour = consumption / hours_elapsed

        to_convert.append({'time': time_anchor, 'consumption': kw_per_hour})            
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