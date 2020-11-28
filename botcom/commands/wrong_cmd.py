from commands.base import Command
from messengers import Messenger


class WrongCmdCommand(Command):
    def execute(self):
        sender = self.msg.sender

        messenger_from = Messenger.get_instance(sender.messenger)
        messenger_from.send(sender.id, None)
