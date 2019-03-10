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
    urlopen(api_url)


def parse(data):
    if 'message' in data:
        msg = data['message']
        name = f"{msg['from']['first_name']} {msg['from']['last_name']}"
        return {
            'real_id': str(msg['from']['id']),
            'msg': msg['text'],
            'name': name,
            'social': NAME
        }
    else:
        return ''
