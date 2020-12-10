import os
from deta import Deta
from dataclasses import asdict
from typing import Dict, Union
import entities

_deta = None


class Storage:
    def __init__(self):
        global _deta
        if _deta is None:
            _deta = Deta(os.getenv('DETA_PROJECT_KEY'))
        self.users = _deta.Base('users')

    def add_user(self, user: 'entities.User'):
        user_dict = asdict(user)
        user_dict.pop('key', None)
        return self.users.put(user_dict)['key']

    def get_user(self, key: str) -> 'entities.User':
        user_db = self.users.get(key)
        return entities.User(**user_db, refine=False)

    def find_user(self, messenger: str, id_: str) -> 'entities.User':
        users = next(self.users.fetch([
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
        return entities.User(**users[0], refine=False) if users else None

    def update(self, key: str, updates: Dict[str, Union[str, None]]):
        return self.users.update(updates, key)

    def get_connected(self, key: str):
        users = next(self.users.fetch({
            'receiver': key
        }))

        return [entities.User(**user, refine=False) for user in users]

    def delete(self, key):
        return self.users.delete(key)
