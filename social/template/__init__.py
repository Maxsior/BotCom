from urllib.parse import urlencode
from urllib.request import urlopen
from config import keys  # You needn't add your key in config

_, NAME = __name__.split('.')


def send_message(real_id, msg, **kwargs):
    """Describe sending in this function"""
    api_url = f"https://api.example.org/send?"  # 1. Put api url
    query = {  # 2. Set options
        'to': real_id,
        'token': keys[NAME],
        'text': msg
    }
    if 'keyboard' in kwargs:
        keyboard = f"./social/{NAME}/{kwargs['keyboard']}_keyboard.json"
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
        'social': NAME
    }


# Please, make others function private with underline
def _extra():
    pass
