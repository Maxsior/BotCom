import os
from deta import Deta
from dataclasses import asdict
from typing import Dict, Union
import entities


class Storage:
    __instance = False

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            deta = Deta(os.getenv('DETA_PROJECT_KEY'))
            cls.__instance.users = deta.Base('users')
        return cls

    def add_user(self, user: 'entities.User'):
        return self.users.put(asdict(user))

    def get_user(self, key) -> 'entities.User':
        user_db = self.users.get(key)
        return entities.User(**user_db)

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
        return entities.User(**users[0]) if users else None

    def update(self, key: str, updates: Dict[str, Union[str, None]]):
        return self.users.update(updates, key)
