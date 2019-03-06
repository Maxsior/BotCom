import os.path
import random
import json
from urllib.parse import urlencode
from urllib.request import urlopen
from config import keys

NAME = 'vk'


def send_message(real_id, msg):
    # TODO настроить клавиатуры
    os.path.join(os.path.dirname(__file__), 'vk_main_keyboard.json')
    api_url = 'https://api.vk.com/method/messages.send?'
    query = urlencode({
        "user_id": real_id,
        "message": msg,
        "access_token": keys[NAME],
        "random_id": random.randint(0, 2**32),
        "v": 5.92
    })
    api_url += query
    # TODO обработать ответ
    with urlopen(api_url) as res:
        print(res.read().decode('utf-8'))


def parse(data):
    data_type = data['type']
    if data_type == 'message_new':
        msg = data['object']
        return {
            'real_id': str(msg['from_id']),
            'msg': msg['text'],
            'social': NAME
        }
    elif data_type == 'confirmation' and data.get('group_id') == 176977577:
        return keys['vk_confirmation']
    else:
        return ''


def get_name(real_id):
    api_url = 'https://api.vk.com/method/users.get?'
    query = urlencode({
        "user_ids": real_id,
        "access_token": keys[NAME],
        "v": 5.92
    })
    api_url += query
    with urlopen(api_url) as res:
        result = json.loads(res.read().decode('utf-8'))["response"][0]
    return result["first_name"] + " " + result["second_name"]
