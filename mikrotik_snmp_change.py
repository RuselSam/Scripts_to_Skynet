#!/usr/bin/env python3

from netmiko import ConnectHandler
from sys import argv
import getpass

def login(ip, user, password):
    device = {
        'device_type': 'mikrotik_routeros',
        'host': ip,
        'username': user,
        'password': password,
    }
    conn = ConnectHandler(**device)
    return conn

if __name__ == '__main__':
    ip = argv[1]
    user = argv[2]
    password = getpass.getpass()
    connection = login(ip, user, password)
    print(connection.find_prompt())
    cmd = connection.send_command('/snmp set contact=noc@skynet-kazan.com enabled=yes location=x\n')
    cmd1 = connection.send_command('/snmp community set [ find default=yes ] address=10.3.0.0/16 name=PUB_SKY \n')

