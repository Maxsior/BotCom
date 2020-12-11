import json
import os
from dataclasses import asdict
import requests
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

        if keyboard is not None:
            query['reply_markup'] = Telegram.create_keyboard(keyboard)

        return requests.post(api_url, data=query)

    @staticmethod
    def create_keyboard(keyboard: Keyboard):
        json_keyboard = {
            'inline_keyboard': []
        }

        row = []
        for button in keyboard.buttons:
            if button:
                row.append({
                    "text": button.text,
                    "callback_data": json.dumps(asdict(button.cmd))
                })
            else:
                json_keyboard['inline_keyboard'].append(row)
                row = []

        return json.dumps(json_keyboard)

    @staticmethod
    def parse(data):
        if 'message' in data or 'callback_query' in data:
            msg = data.get('message') or data.get('callback_query')
            name = msg['from']['first_name']
            if 'last_name' in msg['from']:
                name += f" {msg['from']['last_name']}"

            user = User(
                id=msg['from']['id'],
                name=name,
                messenger='telegram',
                nick=msg['from'].get('username'),
                lang=msg['from'].get('language_code')
            )

            return Message(
                sender=user,
                text=msg.get('text', ''),
                cmd=Telegram.parse_cmd(msg),
                attachments=[]
            )
        else:
            return None

    @staticmethod
    def parse_cmd(msg):
        cmd = None
        if 'data' in msg:
            cmd = CommandInfo(**json.loads(msg['data']))
        elif 'text' in msg and msg['text'].startswith('/'):
            [name, *args] = msg['text'].split()
            cmd = CommandInfo(
                name=name.replace('/', ''),
                args=args
            )
        return cmd
