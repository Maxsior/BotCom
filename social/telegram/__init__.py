from config import keys
import storage
from urllib.parse import urlencode
from urllib.request import urlopen


# TODO Написать методы для отправки и парса сообщение как в vk.py


def send_message(real_id, msg):
    api_url = 'https://api.telegram.org/bot tMe'

    api_url = f"https://api.telegram.org/bot{keys['telegram']}/sendMessage?"
    query = urlencode({
        "chat_id": real_id,
        "text": msg
    })
    api_url += query

    # TODO обработать ответ

    with urlopen(api_url) as res:
        print(res.read().decode('utf-8'))



def parse(data):
    if 'message' in data:
        msg = data['message']

        return {
            'real_id': msg['from']['id'],
            'msg': msg['text'],
            'social': 'telegram'
        }
    else:
        return ''

