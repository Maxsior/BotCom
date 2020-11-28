from commands.base import Command
from messengers import Messenger


class HelpCommand(Command):
    def execute(self):
        messenger = Messenger.get_instance(self.msg.sender.messenger)
        messenger.send(self.msg.sender.id, None)
