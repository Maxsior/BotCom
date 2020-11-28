import os
import random
import json
from urllib.parse import urlencode
from urllib.request import urlopen

from dtos import Message, User, CommandInfo
from messengers import Messenger


class Vk(Messenger):
    @staticmethod
    def send(receiver_id, msg: Message, **kwargs):
        api_url = 'https://api.vk.com/method/messages.send?'
        query = {
            'peer_id': receiver_id,
            'message': msg.text,
            'access_token': os.getenv('VK_TOKEN'),
            'random_id': random.randint(0, 2**32),
            'v': 5.92
        }

        # if 'keyboard' in kwargs:
        #     keyboard = os.path.join(os.path.dirname(__file__), f"{kwargs['keyboard']}_keyboard.json")
        #     with open(keyboard, encoding='utf-8') as f:
        #         query['keyboard'] = f.read()

        api_url += urlencode(query)
        return urlopen(api_url)

    @staticmethod
    def parse(data):
        data_type = data['type']
        if data_type == 'message_new':
            msg = data['object']

            name, nick = Vk._get_info(msg['from_id'])
            user = User(
                id=msg['from_id'],
                name=name,
                messenger='vk',
                nick=nick
            )

            return Message(
                sender=user,
                text=msg['text'],
                cmd=Vk.parse_cmd(msg),
                attachments=[]  # TODO attachments
            )
        elif data_type == 'confirmation' and data.get('group_id') == 176977577:
            return os.getenv('VK_CONFIRMATION')
        else:
            return None

    @staticmethod
    def parse_cmd(msg):
        cmd = None
        if msg['text'].startswith('/'):
            [name, *args] = msg['text'].split()
            cmd = CommandInfo(
                name=name.replace('/', ''),
                args=args
            )
        elif 'payload' in msg:
            payload = json.loads(msg['payload'])
            cmd = CommandInfo(
                name=payload['name'],
                args=payload['args']
            )
        return cmd

    @staticmethod
    def _get_info(real_id):
        api_url = 'https://api.vk.com/method/users.get?'
        query = urlencode({
            'user_ids': real_id,
            'fields': 'domain',
            'access_token': os.getenv('VK_TOKEN'),
            'v': 5.92
        })
        api_url += query
        with urlopen(api_url) as res:
            result = json.loads(res.read().decode('utf-8'))['response'][0]
        return result['first_name'] + ' ' + result['last_name'], result['domain']
