from messengers import Messenger
from entities import Message, User, Keyboard


class Discord(Messenger):
    @staticmethod
    def is_cmd(msg: Message):
        return msg.text.startswith('?b')

    @staticmethod
    def create_keyboard(keyboard):
        pass

    @staticmethod
    def send(id_to: int, message: Message, keyboard: Keyboard = None):
        pass

    @staticmethod
    def parse(data) -> Message:
        user = User(
            id=123,
            nick='nick',
            name='Name Surname',
            messenger='discord'
        )
        return Message(
            sender=user,
            text=data['text'],
            attachments=[]
        )
