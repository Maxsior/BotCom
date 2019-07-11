from urllib.request import Request, urlopen
import json
from config import keys

NAME = __name__[7:]


def send_message(real_id, msg, **kwargs):
    api_url = 'https://chatapi.viber.com/pa/send_message'
    query = {
        'receiver': real_id,
        'message': msg,
        'sender': {
            'name': 'BotCom'
            # 'avatar': ''
        },
        'type': 'text',
        'text': msg
    }
    if 'keyboard' in kwargs:
        keyboard = f"./social/{NAME}/{kwargs['keyboard']}_keyboard.json"
        with open(keyboard, encoding='utf-8') as f:
            query['keyboard'] = f.read()

    r = Request(api_url, json.dumps(query).encode('utf-8'))
    r.add_header('X-Viber-Auth-Token', keys['viber'])
    return urlopen(r)


def parse(data):
    event = data['event']
    if event == 'message':
        user = data['sender']
        msg = data['message']
        return {
            'real_id': str(user['id']),
            'name': user['name'],
            'nick': None,
            'msg': msg['text'],
            'social': NAME
        }
    else:
        return ''
