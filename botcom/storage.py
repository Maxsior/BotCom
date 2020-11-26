from deta import Deta
import os
from dataclasses import asdict
from .dtos import User


class Storage:
    deta = Deta(os.getenv('DETA_PROJECT_KEY'))
    users = deta.Base('users')

    @staticmethod
    def get_receiver_id(sender_id):
        return Storage.users.get(sender_id)['current']

    @staticmethod
    def add_user(user: User):
        return Storage.users.put(asdict(user))
