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


zabauthnew = get_auth(new_zabbix)
REQUEST_DATA = '{ "jsonrpc": "2.0", "auth": "' + zabauthnew + '", "id": "1", "method": "user.create", "params": {"username": "test", "passwd": "test", "name": "test", "surname": "test", "roleid": "1", "usrgrps": [ { "usrgrpid": "8" } ] } }'
r = requests.post(new_zabbix, data=REQUEST_DATA, headers=headers)
print(r.text)
