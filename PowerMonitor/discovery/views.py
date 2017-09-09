# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_list_or_404
from django.http import JsonResponse
from monitor.models import Meter

def index(request):
    return render(request, 'discovery-index.html')

def meters(request):
    db_meters = get_list_or_404(Meter)

    meter_list = []
    meters = {'meters': meter_list}

    for meter in db_meters:
        meter_list.append({
            'meter_id': meter.id,
            'meter_type': meter.type_description()
        })

    return JsonResponse(meters)