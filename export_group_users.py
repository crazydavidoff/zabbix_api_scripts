import requests
import json

user = ""
password = ""
old_zabbix = ""
new_zabbix = ""


headers = { 'content-type': 'application/json-rpc' }

def get_auth(url):
    REQUEST_DATA = '{ "params": { "user": "' + user + '", "password": "' + password + '" }, "jsonrpc": "2.0", "method": "user.login", "id": 0 }'

    r = requests.post(url, data=REQUEST_DATA, headers=headers)
    if r.status_code != 200:
        return None
    return r.json()["result"]

def get_count_groups(auth):
    REQUEST_DATA = '{ "jsonrpc": "2.0", "auth": "' + auth + '", "id": 1, "method": "usergroup.get","params": {"countOutput": "true"} }'

    r = requests.post(old_zabbix, data=REQUEST_DATA, headers=headers)
    if r.status_code != 200:
        return None
    return r.json()["result"]

zabauth = get_auth(old_zabbix)
count_groups = get_count_groups(zabauth)
n = 0
i = 2
groups = []

while n < int(count_groups):
    REQUEST_DATA = '{ "jsonrpc": "2.0", "auth": "' + zabauth + '", "id": "' + str(i) + '", "method": "usergroup.get","params": {"users_status": "0"} }'

    r = requests.post(old_zabbix, data=REQUEST_DATA, headers=headers)
    groups.append(r.json()["result"][n]["name"])

    n += 1
    i += 1

print(groups)
zabauthnew = get_auth(new_zabbix)

j = 1
for group in groups:

    REQUEST_DATA = '{ "jsonrpc": "2.0", "auth": "' + zabauthnew + '", "id": "' + str(j) + '", "method": "usergroup.create","params": {"name": "' + group + '"} }'
    r = requests.post(new_zabbix, data=REQUEST_DATA, headers=headers)
    j += 1
