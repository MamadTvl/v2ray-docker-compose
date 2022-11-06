#!/usr/bin/python3

import base64
import json
import re
from pathlib import Path
from urllib.request import urlopen

path = Path(__file__).parent
file = open(str(path.joinpath('config/config.json')), 'r', encoding='utf-8')
config = json.load(file)

html = open(str(path.joinpath('web/index.html')), 'r', encoding="utf-8").read()

ip = urlopen("http://ifconfig.io/ip").read().decode().rstrip()

for inbound in config['inbounds']:
    if inbound['protocol'] == 'socks':
        print("SOCKS: 127.0.0.1:{}".format(str(inbound['port'])))
    if inbound['protocol'] == 'http':
        print("HTTP: 127.0.0.1:{}".format(str(inbound['port'])))
    if inbound['protocol'] == 'shadowsocks':
        port = str(inbound['port'])
        method = inbound['settings']['method']
        password = inbound['settings']['password']
        security = base64.b64encode((method + ":" + password).encode('ascii')).decode('ascii')
        link = "ss://{}@{}:{}#{}:{}".format(security, ip, port, ip, port)
        print("\nShadowsocks:\n" + link)
        html = re.sub(r'(ss://[^<]+)', link, html)
    if inbound['protocol'] == 'vmess':
        port = str(inbound['port'])
        uuid = inbound['settings']['clients'][0]['id']
        security = inbound['settings']['clients'][0]['security']
        ps = "{}:{}".format(ip, port)
        c = {"add": ip, "aid": "0", "host": "", "id": uuid, "net": "tcp", "path": "", "port": port, "ps": ps,
             "tls": "none", "type": "none", "v": "2"}
        j = json.dumps(c)
        link = "vmess://" + base64.b64encode(j.encode('ascii')).decode('ascii')
        print("\nVMESS:\n" + link)
        html = re.sub(r'(vmess://[^<]+)', link, html)

open(str(path.joinpath('web/index.html')), 'w', encoding='utf-8').write(html)