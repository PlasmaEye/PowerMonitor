from celery import shared_task
from monitor.models import Meter
import subprocess
import os
import json

@shared_task
def find_meters():
    rtltcp_address = '192.168.1.3:1234'
    program = os.getcwd() + r'/lib/rtlamr'

    rtlamr_exists = os.path.exists(program)

    if rtlamr_exists:
        args = [program, '-server', rtltcp_address, '-format', 'json', '-msgtype', 'SCM', '-unique', '-duration', '30s']

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        json_readings = '[' + out.replace('}}\n', '}},')[:-1] + ']'
        
        meter_readings = json.loads(json_readings)

        for meter_reading in meter_readings:
            message = meter_reading['Message']
            meter, meter_created = Meter.objects.get_or_create(id=message['ID'], defaults={'type': message['Type']})

    else:
        return "rtlamr doesn't exist at " + program

    return readings