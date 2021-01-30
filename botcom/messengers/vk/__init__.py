import os
import random
import json
from fastapi import HTTPException
import requests
from entities import Message, User, CommandInfo
from entities.keyboards import Keyboard
from messengers import Messenger
from dataclasses import asdict


class Vk(Messenger):
    @staticmethod
    def send(receiver_id, msg: Message, keyboard: Keyboard = None):
        api_url = 'https://api.vk.com/method/messages.send?'
        query = {
            'peer_id': receiver_id,
            'message': msg.text,
            'access_token': os.getenv('VK_TOKEN'),
            'random_id': random.randint(0, 2**32),
            'v': 5.126
        }

        if keyboard is not None:
            query['keyboard'] = Vk.create_keyboard(keyboard)

        return requests.post(api_url, data=query)

    @staticmethod
    def create_keyboard(keyboard: Keyboard):
        json_keyboard = {
            "one_time": False,
            "buttons": []
        }

        row = []
        for button in keyboard.buttons:
            if button:
                row.append({
                    "action": {
                      "type": "text",
                      "payload": json.dumps(asdict(button.cmd)),
                      "label": button.text
                    },
                    "color": "primary"
                })
            else:
                json_keyboard['buttons'].append(row)
                row = []

        return json.dumps(json_keyboard)

    @staticmethod
    def parse(data):
        data_type = data['type']
        if data_type == 'message_new':
            msg = data['object']['message']
            client_info = data['object']['client_info']

            name, nick = Vk._get_info(msg['from_id'])
            user = User(
                id=msg['from_id'],
                name=name,
                messenger='vk',
                nick=nick,
                lang=Vk._get_lang(client_info['lang_id'])
            )

            return Message(
                sender=user,
                text=msg['text'],
                cmd=Vk.parse_cmd(msg),
                attachments=[]  # TODO attachments
            )
        elif data_type == 'confirmation' and str(data.get('group_id')) == os.getenv('VK_GROUP'):
            raise HTTPException(status_code=200, detail=os.getenv('VK_CONFIRMATION'))
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
        elif 'payload' in msg and 'name' in msg['payload']:
            payload = json.loads(msg['payload'])
            cmd = CommandInfo(
                name=payload['name'],
                args=payload['args']
            )
        return cmd

    @staticmethod
    def _get_info(real_id):
        api_url = 'https://api.vk.com/method/users.get?'
        res = requests.post(api_url, data={
            'user_ids': real_id,
            'fields': 'domain',
            'access_token': os.getenv('VK_TOKEN'),
            'v': 5.126
        })
        result = res.json()['response'][0]
        return result['first_name'] + ' ' + result['last_name'], result['domain']

    @staticmethod
    def _get_lang(lang_id: int):
        # see https://vk.com/dev/api_requests for language id list
        return [
            'ru',
            'uk',
            'be',
            'en',
            'es',
            'fi',
            'de',
            'it'
        ][lang_id]
