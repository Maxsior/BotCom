import os
import random
import json
from urllib.parse import urlencode
from urllib.request import urlopen

NAME = __name__.split('.')[1]


def send_message(real_id, msg, **kwargs):
    api_url = 'https://api.vk.com/method/messages.send?'
    query = {
        'peer_id': real_id,
        'message': msg,
        'access_token': os.getenv('VK_TOKEN'),
        'random_id': random.randint(0, 2**32),
        'v': 5.92
    }
    if 'keyboard' in kwargs:
        keyboard = f"./messengers/{NAME}/{kwargs['keyboard']}_keyboard.json"
        with open(keyboard, encoding='utf-8') as f:
            query['keyboard'] = f.read()

    api_url += urlencode(query)
    return urlopen(api_url)


def parse(data):
    data_type = data['type']
    if data_type == 'message_new':
        msg = data['object']

        if 'payload' in msg:
            msg['text'] = str(json.loads(msg['payload']))

        name, nick = _get_info(msg['from_id'])
        return {
            'real_id': str(msg['peer_id']),
            'nick': nick,
            'name': name,
            'msg': msg['text'],
            'messengers': NAME
        }
    elif data_type == 'confirmation' and data.get('group_id') == 176977577:
        return os.getenv('VK_CONFIRMATION')
    else:
        return ''


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
