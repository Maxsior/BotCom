import os
from urllib.parse import urlencode
from urllib.request import urlopen
from messengers import Messenger
from dtos import Message, User, CommandInfo


class Telegram(Messenger):
    @staticmethod
    def is_cmd(msg: Message):
        return msg.text.startswith('/')

    @staticmethod
    def send(receiver_id, msg: Message, **kwargs):
        api_url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage?"
        query = {
            'chat_id': receiver_id,
            'text': msg.text
        }

        # if 'keyboard' in kwargs:
        #     keyboard = os.path.join(os.path.dirname(__file__), f"{kwargs['keyboard']}_keyboard.json")
        #     with open(keyboard, encoding='utf-8') as f:
        #         query['reply_markup'] = f.read()

        api_url += urlencode(query)
        return urlopen(api_url)

    @staticmethod
    def parse(data):
        if 'message' in data:
            msg = data['message']
            name = msg['from']['first_name'] + ' ' + msg['from']['last_name']

            user = User(
                id=msg['chat']['id'],
                name=name,
                messenger='telegram',
                nick=msg['from']['username']
            )

            return Message(
                sender=user,
                text=msg['text'],
                cmd=Telegram.parse_cmd(msg)
            )
        else:
            return None

    @staticmethod
    def parse_cmd(msg):
        cmd = None
        if msg['text'].startswith('/'):
            [name, *args] = msg['text'].split()
            cmd = CommandInfo(
                name=name.replace('/', ''),
                args=args
            )
        return cmd
