import itertools as itt
from concurrent.futures import ThreadPoolExecutor
import netmiko
import logging
import csv
import ipaddress
import subprocess as sub

USER = ''
PASSWORD = ''

logging.basicConfig(level=logging.INFO)
logging.getLogger('paramiko').setLevel(logging.WARNING)

device_to_authentificated_faile = []
mikrotik_devices = []
new_mikrotik_devices = []
fail_mikrotik_devices = []

with open('mikrotiks.csv') as file:
    devices = csv.reader(file)
    for device in devices:
        mikrotik_devices.append(device[0].strip())

def ping_to_device(devices):
    for device in devices:
        replay = sub.run(['ping', '-c', '3', '-n', device])
        if replay.returncode == 0:
            new_mikrotik_devices.append(device)
        else:
            fail_mikrotik_devices.append(device)

def send_show(device,login,password, show):
    try:
        with netmiko.ConnectHandler(device_type='mikrotik_routeros', host=device, username=login, password=password) as ssh:
            logging.info(f'Подключение к {device}')
            return ssh.send_command(show)
    except netmiko.NetMikoAuthenticationException as err:
        logging.info('Не подключается ')
        device_to_authentificated_faile.append(device)

ping_to_device(mikrotik_devices)

with ThreadPoolExecutor(max_workers=5) as executor:
    result = executor.map(send_show, new_mikrotik_devices, itt.repeat(USER), itt.repeat(PASSWORD), itt.repeat('/ip add print'))
    for device, output in zip(new_mikrotik_devices, result):
        print(f'Вывод : \n Устройство: {device} \n, {output}')
logging.info(device_to_authentificated_faile)

