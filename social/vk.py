from config import keys
import storage
from urllib.parse import urlencode
from urllib.request import urlopen
import json


def send_message(uid, msg):
    with open("vk_keyboards.json") as f:
        keyboards = json.load(f)
    api_url = 'https://api.vk.com/method/messages.send?'
    query = urlencode({
        "user_id": storage.get_real_id(uid, 'vk'),
        "message": msg,
        "access_token": keys['vk']
    })
    api_url += query
    # TODO обработать ответ
    with urlopen(api_url) as res:
        print(res)


def parse(data):
    # TODO отлов ошибок
    data_type = data['type']
    if data_type == 'message_new':
        return {
            'real_id': data['user_id'],
            'msg': data['body'],
            'social': 'vk'
        }
    elif data_type == 'confirmation':
        if data['group_id'] == 176977577:
            return '894adea0'
        else:
            return ''
