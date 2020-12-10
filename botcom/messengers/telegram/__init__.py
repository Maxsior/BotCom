import os
from urllib.parse import urlencode
from urllib.request import urlopen
from messengers import Messenger
from entities.keyboards import Keyboard
from entities import Message, User, CommandInfo


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
            name = msg['from']['first_name']
            if 'last_name' in msg['from']:
                name += f" {msg['from']['last_name']}"

            user = User(
                id=msg['chat']['id'],
                name=name,
                messenger='telegram',
                nick=msg['from'].get('username'),
                lang=msg['from'].get('language_code')
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
