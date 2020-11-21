from messengers import Messenger
from dtos import Message, User


class Discord(Messenger):
    @staticmethod
    def send(id_to: int, message: Message):
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
