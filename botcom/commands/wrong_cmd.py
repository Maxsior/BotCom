from commands.base import Command
from messengers import Messenger
from dtos import Message
import l10n


class WrongCmdCommand(Command):
    def execute(self):
        sender = self.msg.sender

        messenger_from = Messenger.get_instance(sender.messenger)
        messenger_from.send(sender.id, Message(l10n.format(sender.lang, 'UNDEFINED_CMD')))
