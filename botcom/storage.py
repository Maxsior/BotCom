import os
from deta import Deta
from dataclasses import asdict
from dtos import User


class Storage:
    deta = Deta(os.getenv('DETA_PROJECT_KEY'))
    users = deta.Base('users')

    @staticmethod
    def get_receiver_id(sender_id):
        return Storage.users.get(sender_id)['current']

    @staticmethod
    def add_user(user: User):
        return Storage.users.put(asdict(user))

    @staticmethod
    def find_user(messenger: str, id_: str):
        users = next(Storage.users.fetch([
            {
                'id': id_,
                'messenger': messenger
            },
            {
                'nick': id_,
                'messenger': messenger
            },
            {
                # TODO format phone
                'phone': id_,
                'messenger': messenger
            }
        ]))
        return users[0] if users else None

    @staticmethod
    def update_receiver(sender_key: str, receiver_key: str):
        return Storage.users.update({"receiver": receiver_key}, sender_key)
