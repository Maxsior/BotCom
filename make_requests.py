from http.client import HTTPConnection, RemoteDisconnected
import json


def get(url, port=8080):
    conn = HTTPConnection('localhost', port)
    conn.request('GET', url, headers={'Content-type': 'text/html'})
    try:
        response = conn.getresponse()
        print(response.read().decode())
    except RemoteDisconnected as e:
        print(e)
    conn.close()


def post(data, network_name, port=8080):
    conn = HTTPConnection('localhost', port)
    conn.request(
        'POST',
        '/' + network_name,
        body=json.dumps(data),
        headers={'Content-type': 'application/json'}
    )
    try:
        response = conn.getresponse()
        print(response.read().decode())
    except RemoteDisconnected as e:
        print(e)
    conn.close()


# Пример описания тестовых запросов
# post({"type": "confirmation", "group_id": 176977577}, 'vk')
# post({"type": "message_new", "group_id": 176977577, "user_id": "maxsior777",
# "body": "hello bot"}, 'vk')
# get('/numbers/?one=1&two=2&three=3')
