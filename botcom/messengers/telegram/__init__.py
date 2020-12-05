import os
from urllib.parse import urlencode
from urllib.request import urlopen
from messengers import Messenger
from entities import Message, User, CommandInfo, Keyboard


class Telegram(Messenger):
    @staticmethod
    def send(receiver_id, msg: Message, keyboard: Keyboard = None):
        api_url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage?"
        query = {
            'chat_id': receiver_id,
            'text': msg.text
        }

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
                nick=msg['from']['username'],
                lang=msg['from']['language_code']
            )

            return Message(
                sender=user,
                text=msg.get('text', ''),
                cmd=Telegram.parse_cmd(msg),
                attachments=Telegram.parse_attachments(msg)
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
