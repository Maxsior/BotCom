from config import keys
from urllib.parse import urlencode
from urllib.request import urlopen

NAME = 'telegram'


def send_message(real_id, msg):
    api_url = f"https://api.telegram.org/bot{keys[NAME]}/sendMessage?"
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
            'real_id': str(msg['from']['id']),
            'msg': msg['text'],
            'social': NAME
        }
    else:
        return ''


def get_name(real_id):
    return 'Telegram'
