from commands.base import Command
from storage import Storage
from messengers import Messenger
from entities import Message
import entities.keyboards as keyboards


class OffCommand(Command):
    def execute(self):
        sender = self.msg.sender
        messenger_from = Messenger.get_instance(sender.messenger)
        if sender.receiver is not None:
            receiver = Storage().get_user(sender.receiver)
            Storage().update(sender.key, {'receiver': None})
            Storage().update(receiver.key, {'receiver': None})
            messenger_to = Messenger.get_instance(receiver.messenger)
            messenger_to.send(
                receiver.id,
                Message('MESSAGE.FRIEND_OFF').localize(receiver.lang),
                keyboards.ConnectKeyboard(receiver)
            )
            messenger_from.send(
                sender.id,
                Message('MESSAGE.OFF').localize(sender.lang),
                keyboards.ConnectKeyboard(sender)
            )
        else:
            messenger_from.send(
                sender.id,
                Message('MESSAGE.OFF_BLANK').localize(sender.lang),
                keyboards.ConnectKeyboard(sender)
            )
