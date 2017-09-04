from celery import shared_task
from models import Meter, Reading
import subprocess
import os
import json
import dateutil.parser

@shared_task
def recordReading():
    rtltcp_address = '192.168.1.3:1234'
    program = os.getcwd() + r'/lib/rtlamr'
    args = [program, '-server', rtltcp_address, '-format', 'json', '-filterid', '64633980', '-msgtype', 'SCM', '-single']

    rtlamr_exists = os.path.exists(program)

    if rtlamr_exists:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        
        reading = json.loads(out)

        time = dateutil.parser.parse(reading['Time'])
        message = reading['Message']
        message_id = message['ID']
        meter_consumption = message['Consumption']
        meter_type = message['Type']

        meter, meter_created = Meter.objects.get_or_create(id=message_id, defaults={'type': meter_type})

        reading, reading_created = Reading.objects.get_or_create(consumption=meter_consumption, meter=meter, defaults={'time': time})

        if meter_created and reading_created:
            return 'Meter and Reading created'
        elif reading_created:
            return 'Reading created, consumption: ' + str(meter_consumption)
        else:
            return 'Meter and Reading already exist, nothing done'
    else:
        return program + " doesn't exist"