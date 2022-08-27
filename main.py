import sys,os
import requests
from playsound import playsound
import time
from datetime import datetime

slash="/"

if sys.platform == 'windows':
    slash="\\"
else:
    slash="/"

failed=False

options={
    "log": {
        "filename_format":'pinger.%Y-%m-%d.%H-%M-%S.log',
        "dir":"logs",
        "time_format":'%m/%d/%Y %H:%M:%S'
    },
    "output": {
        "send_char":'.',
        "success_char":'!',
        "fail_char":'x',
    },
    "site":"https://1.1.1.1/",
    "timeout":5,
    "sleep_after_success":15,
    "sleep_after_fail":2,
}

now=datetime.now()

with open(options["log"]["dir"] + slash + now.strftime(options["log"]["filename_format"]),'w') as f:
    while True:
        try:
            print(options["output"]['send_char'],end="")
            sys.stdout.flush()

            r = requests.get(options["site"],timeout=options["timeout"])

            print(options["output"]['success_char'],end="")
            sys.stdout.flush()

            if failed:
                now=datetime.now()
                f.write(f"[{now.strftime(options['log']['time_format'])}] Connection to {options['site']} recovered!\n")
                playsound(os.getcwd()+f"{slash}reconnect.mp3")

            time.sleep(options["sleep_after_success"])
            failed=False

        except Exception as e:
            now=datetime.now()

            if not failed:
                f.write(f"[{now.strftime(options['log']['time_format'])}] Connection to {options['site']} failed. Error: {str(e)}\n")

            playsound(os.getcwd()+"\\beep.mp3")

            print(options["output"]['fail_char'],end="")
            sys.stdout.flush()

            time.sleep(options["sleep_after_fail"])
            failed=True
