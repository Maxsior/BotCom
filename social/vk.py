from config import keys
import storage
from urllib.parse import urlencode

# TODO отлов ошибок в функции parse


def send_message(uid, msg):
    api_url = 'https://api.vk.com/method/messages.send?'
    query = urlencode({
        "user_id": storage.get_real_id(uid, 'vk'),
        "message": msg,
        "access_token": keys['vk']
    })
    api_url += query
    # TODO выполнить этот запрос


def parse(data):
    data_type = data['type']
    if data_type == 'message_new':
        return {
            'uid': data['user_id'],
            'msg': data['body']
        }
    elif data_type == 'confirmation':
        if data['group_id'] == 176977577:
            return '894adea0'
        else:
            return ''
