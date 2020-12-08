from commands.base import Command
from messengers import Messenger
from entities import Message
import l10n


class WrongCmdCommand(Command):
    def execute(self):
        sender = self.msg.sender

        if sender.registered:
            messenger_from = Messenger.get_instance(sender.messenger)
            messenger_from.send(sender.id, Message('MESSAGE.UNDEFINED_CMD').localize(sender.lang))
