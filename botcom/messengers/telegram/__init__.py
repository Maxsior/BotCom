import os
from urllib.parse import urlencode
from urllib.request import urlopen

NAME = __name__.split('.')[1]


def send_message(real_id, msg, **kwargs):
    api_url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage?"
    query = {
        'chat_id': real_id,
        'text': msg
    }
    if 'keyboard' in kwargs:
        keyboard = f"./messengers/telegram/{kwargs['keyboard']}_keyboard.json"
        with open(keyboard, encoding='utf-8') as f:
            query['reply_markup'] = f.read()
    api_url += urlencode(query)
    return urlopen(api_url)


def parse(data):
    if 'message' in data:
        msg = data['message']
        name = msg['from']['first_name'] + ' ' + msg['from']['last_name']
        return {
            'real_id': str(msg['chat']['id']),
            'nick': msg['from']['username'],
            'name': name,
            'msg': msg['text'],
            'messengers': NAME
        }
    else:
        return ''
