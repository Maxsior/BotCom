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
post({
    'type': 'message_new',
    'object': {
        'from_id': 188482059,
        'text': '/status'
    }
}, 'vk')
