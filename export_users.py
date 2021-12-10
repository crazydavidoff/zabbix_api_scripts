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

def get_count_users(auth):
    REQUEST_DATA = '{ "jsonrpc": "2.0", "auth": "' + auth + '", "id": 1, "method": "user.get","params": {"countOutput": "true"} }'

    r = requests.post(old_zabbix, data=REQUEST_DATA, headers=headers)
    if r.status_code != 200:
        return None
    return r.json()["result"]

zabauth = get_auth(old_zabbix)
zabauthnew = get_auth(new_zabbix)
count_users = get_count_users(zabauth)
n = 0
i = 2
j = 1
while n < int(count_users):
    REQUEST_DATA = '{ "jsonrpc": "2.0", "auth": "' + zabauth + '", "id": "i", "method": "user.get","params": {"sortfield ": "userid"} }'

    r = requests.post(old_zabbix, data=REQUEST_DATA, headers=headers)

    username = r.json()["result"][n]["alias"]
    name = r.json()["result"][n]["name"]
    surname = r.json()["result"][n]["surname"]

    REQUEST_DATA = '{ "jsonrpc": "2.0", "auth": "' + zabauthnew + '", "id": "' + str(j) + '", "method": "user.create", "params": {"username": "' + username + '", "passwd": "12345", "name": "' + name + '", "surname": "' + surname + '", "roleid": "1", "usrgrps": [ { "usrgrpid": "8" } ] } }'
    REQUEST_DATA = REQUEST_DATA.encode("utf-8")
    r = requests.post(new_zabbix, data=REQUEST_DATA, headers=headers)
    print(r.text)
    n += 1
    i += 1
    j += 1

