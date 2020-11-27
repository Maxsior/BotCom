import os
from urllib.request import Request, urlopen
import json
from messengers import Messenger
from dtos import Message


class Viber(Messenger):
    @staticmethod
    def is_cmd(msg: Message):
        return msg.text.startswith('/')

    @staticmethod
    def send(real_id, msg, **kwargs):
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
            keyboard = os.path.join(os.path.dirname(__file__), f"{kwargs['keyboard']}_keyboard.json")
            with open(keyboard, encoding='utf-8') as f:
                query['keyboard'] = f.read()

        r = Request(api_url, json.dumps(query).encode('utf-8'))
        r.add_header('X-Viber-Auth-Token', os.getenv('VIBER_TOKEN'))
        return urlopen(r)

    @staticmethod
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
                'messengers': 'vk'
            }
        else:
            return ''
