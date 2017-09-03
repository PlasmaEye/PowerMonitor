from celery import shared_task
from models import Meter, Reading
import subprocess
import os
import json
import dateutil.parser

@shared_task
def recordReading():
    program = os.getcwd() + r'/lib/rtlamr'
    args = [program, '-server', '192.168.1.3:1234', '-format', 'json', '-filterid', '64633980', '-msgtype', 'SCM', '-single']    

    rtlamrExists = os.path.exists(program)    

    if(rtlamrExists):
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        reading = json.loads(out)

        time = dateutil.parser.parse(reading['Time']) 
        message = reading['Message']
        id = message['ID']
        consumption = message['Consumption']
        type = message['Type']

        meter, created = Meter.objects.get_or_create(id=id, defaults={'type': type})
        
        reading = Reading.objects.get_or_create(consumption=consumption, meter=meter, defaults={'time': time})

        return json.dumps({ 'output' : out, 'error' : err })
    else:
        return program + " doesn't exist"