import os.path
import random
from urllib.parse import urlencode
from urllib.request import urlopen
from config import keys


def send_message(real_id, msg):
    # TODO настроить клавиатуры
    os.path.join(os.path.dirname(__file__), 'vk_main_keyboard.json')
    api_url = 'https://api.vk.com/method/messages.send?'
    query = urlencode({
        "user_id": real_id,
        "message": msg,
        "access_token": keys['vk'],
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
            'real_id': msg['user_id'],
            'msg': msg['body'],
            'social': 'vk'
        }
    elif data_type == 'confirmation' and data.get('group_id') == 176977577:
        return keys['vk_confirmation']
    else:
        return ''
