import os
from urllib.parse import urlencode
from urllib.request import urlopen

# __name__ is 'messengers.template'
# but we need only second part
NAME = __name__.split('.')[1]


def send_message(real_id, msg, **kwargs):
    """Describe sending in this function"""
    api_url = 'https://api.example.org/send?'  # 1. Put api url
    query = {  # 2. Set options
        'to': real_id,
        'token': os.getenv('MY_TOKEN'),
        'text': msg
    }
    if 'keyboard' in kwargs:
        keyboard = f"./messengers/{NAME}/{kwargs['keyboard']}_keyboard.json"
        with open(keyboard, encoding='utf-8') as f:
            query['keyboard'] = f.read()  # 3. Set keyboard option
    api_url += urlencode(query)
    return urlopen(api_url)


def parse(data):
    """This function must return dictionary with fields specified below"""
    return {
        'real_id': str(),  # IMPORTANT! real_id must be string
        'nick': '',
        'name': '',
        'msg': '',
        'messengers': NAME
    }


# Please, make others function private with underline
def _extra():
    pass
