from commands import Command


class HelpCommand(Command):
    def execute(self):
        self.messenger.send(self.msg.sender.id, None)
