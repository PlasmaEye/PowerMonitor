from celery import shared_task
import subprocess
import os
import json

@shared_task
def find_meters():
    rtltcp_address = '192.168.1.3:1234'
    program = os.getcwd() + r'/lib/rtlamr'

    rtlamr_exists = os.path.exists(program)

    if rtlamr_exists:
        args = [program, '-server', rtltcp_address, '-format', 'json', '-msgtype', 'SCM', '-unique', '-duration', '1m']

        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()

        jsonReadings = '[' + out.replace('\n', ',') + ']'
        print jsonReadings
        readings = json.loads(out)
    else:
        return "rtlamr doesn't exist at " + program

    return readings