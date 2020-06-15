import logging
import csv
import subprocess as sub
import concurrent.futures as conc
import itertools as itt

mikrotik_devices = []
new_mikrotik_devices = []
fail_mikrotik_devices = []

logging.basicConfig(level=logging.INFO)
logging.getLogger('paramiko').setLevel(logging.WARNING)

with open('mikrotiks.csv') as file:
    devices = csv.reader(file)
    for device in devices:
        mikrotik_devices.append(device[0].strip())

print(mikrotik_devices)

def ping_to_device(devices):
    for device in devices:
        replay = sub.run(['ping', '-c', '3', '-n', device])
        logging.info(f'ping to device {device}')
        if replay.returncode == 0:
            new_mikrotik_devices.append(device)
            logging.info(f'ping to device {device}')
        else:
            fail_mikrotik_devices.append(device)
    print(fail_mikrotik_devices)

##with conc.ThreadPoolExecutor(max_workers=1) as executor_ping:
##   result_to_ping = executor_ping.map(ping_to_device, itt.repeat(mikrotik_devices))

ping_to_device(mikrotik_devices)
print(new_mikrotik_devices)
print(fail_mikrotik_devices)