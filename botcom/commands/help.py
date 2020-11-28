from commands.base import Command
from messengers import Messenger
from dtos import Message
import l10n


class HelpCommand(Command):
    def execute(self):
        sender = self.msg.sender
        messenger = Messenger.get_instance(sender.messenger)
        messenger.send(sender.id, Message(l10n.format(sender.lang, 'FULL_HELP')))
