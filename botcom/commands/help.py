from commands.base import Command
from messengers import Messenger
from entities import Message
import entities.keyboards as keyboards


class HelpCommand(Command):
    def execute(self):
        sender = self.msg.sender
        messenger = Messenger.get_instance(sender.messenger)
        messenger.send(
            sender.id,
            Message('MESSAGE.FULL_HELP').localize(sender.lang),
            keyboards.ConnectKeyboard(sender)
        )
