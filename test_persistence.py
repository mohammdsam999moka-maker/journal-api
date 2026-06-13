import json
from urllib import request

url = 'http://127.0.0.1:8000/notes'
data = json.dumps({'title': 'Test note', 'content': 'Persistence test'}).encode('utf-8')
req = request.Request(url, data=data, headers={'Content-Type': 'application/json'})
with request.urlopen(req) as resp:
    print('POST', resp.status, resp.read().decode())
with request.urlopen(url) as resp:
    print('GET', resp.status, resp.read().decode())
