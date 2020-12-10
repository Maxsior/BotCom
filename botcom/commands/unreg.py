from commands.base import Command
from storage import Storage
from messengers import Messenger
from entities import Message
import entities.keyboards as keyboards


class UnregCommand(Command):
    def execute(self):
        sender = self.msg.sender

        for connected in sender.connections:
            Storage().update(connected.key, {'receiver': None})
            messenger_to = Messenger.get_instance(connected.messenger)
            messenger_to.send(
                connected.id,
                Message('MESSAGE.FRIEND_OFF').localize(connected.lang),
                keyboards.StartKeyboard(connected)
            )

        Storage().delete(sender.key)
        messenger = Messenger.get_instance(sender.messenger)
        messenger.send(
            sender.id,
            Message('MESSAGE.BYE').localize(sender.lang, messenger=sender.messenger),
            keyboards.StartKeyboard(sender)
        )
