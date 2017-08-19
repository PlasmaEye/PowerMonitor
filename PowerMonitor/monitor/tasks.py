from celery import shared_task
from models import Meter, Reading
import subprocess
import os
import json
import datetime

@shared_task
def recordReading():
    program = os.getcwd() + r'/lib/rtlamr'
    args = [program, '-server', '192.168.1.3:1234', '-format', 'json', '-filterid', '64633980', '-msgtype', 'SCM', '-single']    

    rtlamrExists = os.path.exists(program)    

    if(rtlamrExists):
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        reading = json.loads(out)

        time = time.strptime(reading['Time'], 
        message = reading['Message']
        id = message['ID']
        consumption = message['Consumption']
        type = message['Type']

        print reading.keys()
        print 'time: ' + time
        print 'consumption: ' + str(consumption)

        Meter.objects

        return out, err
    else:
        return program + ' doesn\'t exist'